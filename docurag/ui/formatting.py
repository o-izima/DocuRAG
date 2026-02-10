from typing import Dict, List

def format_sources(metas: List[Dict], max_chars: int = 300) -> str:
    if not metas:
        return "No citations."
    lines = ["### 📚 Sources"]
    seen = set()
    for m in metas:
        raw = (m.get("text") or "").replace("\n", " ").strip()
        key = (m.get("source"), m.get("page"), raw[:120])
        if key in seen:
            continue
        seen.add(key)
        if len(raw) > max_chars:
            cut = raw.rfind(" ", 0, max_chars)
            cut = cut if cut != -1 else max_chars
            raw = raw[:cut].rstrip() + "..."
        lines.append(f'- **{m.get("source","Unknown")}** (Page {m.get("page","?")}): "{raw}"')
    return "\n".join(lines)

def format_debug_retrieval(docs: List[str], metas: List[Dict], max_chars: int = 450) -> str:
    if not docs:
        return "No retrieved chunks (empty retrieval result)."
    lines = ["### 🧪 Retrieval Debug (Top-K Chunks)"]
    for i, (d, m) in enumerate(zip(docs, metas), start=1):
        raw = (d or "").replace("\n", " ").strip()
        if len(raw) > max_chars:
            cut = raw.rfind(" ", 0, max_chars)
            cut = cut if cut != -1 else max_chars
            raw = raw[:cut].rstrip() + "..."
        lines.append(
            f"**{i}. {m.get('source','Unknown')} — Page {m.get('page','?')}**\n\n"
            f"> {raw}\n"
        )
    return "\n\n".join(lines)
