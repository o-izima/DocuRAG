from typing import List, Dict
from docurag.utils.text import clean_text
from docurag.utils.nlp import safe_sentence_split

def chunk_word_window(
    text: str,
    source_name: str,
    page_num: int,
    chunk_words: int = 180,
    overlap: int = 40
) -> List[Dict]:
    """Fixed-size word windows with overlap; robust for long/OCR text."""
    words = clean_text(text).split()
    chunks: List[Dict] = []
    step = max(1, chunk_words - overlap)
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_words]).strip()
        if len(chunk) < 120:
            continue
        chunks.append({"source": source_name, "page": page_num + 1, "text": chunk})
    return chunks

def chunk_sentence_based(
    text: str,
    source_name: str,
    page_num: int,
    max_words: int = 220
) -> List[Dict]:
    """Sentence-preserving chunking; better citations/summaries."""
    text = clean_text(text)
    sentences = [s.strip() for s in safe_sentence_split(text) if len(s.strip()) > 20]
    chunks: List[Dict] = []
    current: List[str] = []
    current_words = 0

    for sent in sentences:
        w = len(sent.split())
        if w > max_words:
            sent = " ".join(sent.split()[:max_words])
            w = len(sent.split())

        if current_words + w > max_words and current:
            chunks.append({"source": source_name, "page": page_num + 1, "text": " ".join(current)})
            current = []
            current_words = 0

        current.append(sent)
        current_words += w

    if current:
        chunks.append({"source": source_name, "page": page_num + 1, "text": " ".join(current)})

    return chunks

def chunk_text(
    text: str,
    source_name: str,
    page_num: int,
    mode: str = "auto"
) -> List[Dict]:
    """Unified chunking controller.

    mode:
      - 'word'     -> word-window chunking
      - 'sentence' -> sentence-preserving chunking
      - 'auto'     -> heuristic selection
    """
    if mode == "word":
        return chunk_word_window(text, source_name, page_num)
    if mode == "sentence":
        return chunk_sentence_based(text, source_name, page_num)

    wc = len(clean_text(text).split())
    if wc > 900:
        return chunk_word_window(text, source_name, page_num)
    return chunk_sentence_based(text, source_name, page_num)
