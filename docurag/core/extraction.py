from typing import Dict, List, Tuple
import fitz

from docurag.utils.text import clean_text

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except Exception:
    PDFPLUMBER_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    PYTESSERACT_AVAILABLE = True
except Exception:
    PYTESSERACT_AVAILABLE = False

def _ocr_page(page: fitz.Page, dpi: int = 200) -> str:
    """True OCR using pytesseract if available."""
    if not PYTESSERACT_AVAILABLE:
        return ""
    try:
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return clean_text(pytesseract.image_to_string(img))
    except Exception:
        return ""

def extract_pages_with_cascade(file_path: str) -> Tuple[List[str], Dict[str, int]]:
    """Extract per-page text using cascade: fitz -> pdfplumber -> OCR.

    Returns:
      pages_text: list[str] aligned to pages
      stats: counts for fitz/pdfplumber/ocr/empty/pages
    """
    doc = fitz.open(file_path)
    pages_text: List[str] = [""] * len(doc)

    stats = {"pages": len(doc), "fitz": 0, "pdfplumber": 0, "ocr": 0, "empty": 0}

    plumber = None
    if PDFPLUMBER_AVAILABLE:
        try:
            plumber = pdfplumber.open(file_path)
        except Exception:
            plumber = None

    for i in range(len(doc)):
        page = doc[i]
        text = clean_text(page.get_text("text") or "")
        if text.strip():
            pages_text[i] = text
            stats["fitz"] += 1
            continue

        if plumber is not None:
            try:
                t2 = clean_text(plumber.pages[i].extract_text() or "")
            except Exception:
                t2 = ""
            if t2.strip():
                pages_text[i] = t2
                stats["pdfplumber"] += 1
                continue

        t3 = _ocr_page(page)
        if t3.strip():
            pages_text[i] = t3
            stats["ocr"] += 1
            continue

        stats["empty"] += 1

    if plumber is not None:
        try:
            plumber.close()
        except Exception:
            pass
    doc.close()
    return pages_text, stats
