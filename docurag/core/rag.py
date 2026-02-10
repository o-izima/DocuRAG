import uuid
from typing import Dict, List, Tuple
from openai import OpenAI

from docurag.core.chunking import chunk_text
from docurag.core.extraction import extract_pages_with_cascade

SUMMARY_KEYWORDS = [
    "summarize", "summary", "overview", "main contributions", "contributions",
    "key contributions", "what is this paper about", "abstract"
]

def is_summary_intent(query: str) -> bool:
    q = (query or "").lower().strip()
    return any(k in q for k in SUMMARY_KEYWORDS)

def index_document(
    vs_collection,
    file_path: str,
    source_name: str,
    chunk_mode: str = "auto"
) -> Tuple[str, Dict]:
    """Extract -> chunk -> embed/index into Chroma; returns status + stats."""
    pages, ex_stats = extract_pages_with_cascade(file_path)

    all_chunks: List[Dict] = []
    used_modes = {"word": 0, "sentence": 0}

    for page_num, page_text in enumerate(pages):
        if not (page_text or "").strip():
            continue

        if chunk_mode == "auto":
            resolved = "word" if len(page_text.split()) > 900 else "sentence"
        else:
            resolved = chunk_mode

        chunks = chunk_text(page_text, source_name, page_num, mode=chunk_mode)
        all_chunks.extend(chunks)
        if resolved in used_modes:
            used_modes[resolved] += len(chunks)

    if not all_chunks:
        status = (
            "❌ No readable text could be extracted from this PDF. "
            "If it's scanned, enable OCR (tesseract-ocr + pytesseract)."
        )
        stats = {"chunk_mode": chunk_mode, "resolved_modes": [], "chunks": 0, **ex_stats}
        return status, stats

    ids = [uuid.uuid4().hex for _ in all_chunks]
    vs_collection.add(
        documents=[c["text"] for c in all_chunks],
        metadatas=[{"source": c["source"], "page": c["page"], "text": c["text"]} for c in all_chunks],
        ids=ids
    )

    resolved_modes = [k for k, v in used_modes.items() if v > 0] or [chunk_mode]
    resolved = "/".join(resolved_modes)

    status = (
        "✅ Document Indexed Successfully\n"
        f"Chunking used: {chunk_mode} → {resolved} | Chunks: {len(all_chunks)} "
        f"(word: {used_modes['word']}, sentence: {used_modes['sentence']})\n"
        f"Pages: {ex_stats['pages']} | fitz: {ex_stats['fitz']} | pdfplumber: {ex_stats['pdfplumber']} | "
        f"OCR: {ex_stats['ocr']} | empty: {ex_stats['empty']}"
    )
    stats = {"chunk_mode": chunk_mode, "resolved_modes": resolved_modes, "chunks": len(all_chunks), **ex_stats}
    return status, stats

def retrieve(vs_collection, query: str, k: int) -> Tuple[List[str], List[Dict]]:
    q = (query or "").strip()
    if not q:
        return [], []
    res = vs_collection.query(query_texts=[q], n_results=int(k))
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    return docs, metas

def generate_answer(
    client: OpenAI,
    query: str,
    docs: List[str],
    metas: List[Dict],
    chat_model: str
) -> Tuple[str, List[Dict]]:
    if not docs:
        return "The provided context does not contain relevant information.", []

    blocks = []
    for d, m in zip(docs, metas):
        blocks.append(f"[{m.get('source','Unknown')} | Page {m.get('page','?')}] {d[:900]}")
    context = "\n\n".join(blocks)

    summary_mode = is_summary_intent(query)

    if summary_mode:
        system = (
            "You are a research assistant. Produce a concise summary ONLY from the context. "
            "Include: Problem, Method, Main contributions, Results/claims, Limitations. "
            "Cite key statements with [Source, Page X]. If missing, say what's missing."
        )
    else:
        system = (
            "You are a helpful assistant. Answer ONLY using the context. "
            "If the answer is not in the context, say exactly: "
            ""The provided context does not contain relevant information." "
            "Keep answers concise (5-8 sentences)."
        )

    user = f"Context:\n{context}\n\nQuestion:\n{query}"

    resp = client.chat.completions.create(
        model=chat_model,
        temperature=0,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    answer = resp.choices[0].message.content.strip()
    if "does not contain relevant information" in answer.lower():
        return answer, []
    return answer, metas
