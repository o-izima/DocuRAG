import re

def clean_text(text: str) -> str:
    """Normalize PDF-extracted text for better embeddings."""
    if not text:
        return ""
    text = text.replace("-\n", "")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text
