import re
from typing import List
import nltk

def ensure_nltk_resources() -> None:
    """Ensure NLTK tokenizers exist; safe for Codespaces/HF Spaces."""
    for res in ["punkt", "punkt_tab"]:
        try:
            nltk.data.find(f"tokenizers/{res}")
        except LookupError:
            nltk.download(res)

def safe_sentence_split(text: str) -> List[str]:
    """Split into sentences with a regex fallback."""
    try:
        from nltk.tokenize import sent_tokenize
        return sent_tokenize(text)
    except Exception:
        return re.split(r'(?<=[.!?])\s+', text)
