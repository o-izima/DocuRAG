import os
import uuid
import requests
from typing import Optional, Tuple

def download_pdf(url: str, timeout_s: int = 30) -> str:
    """Download a PDF from URL into /tmp and return the local path."""
    resp = requests.get(url, timeout=timeout_s)
    resp.raise_for_status()
    path = f"/tmp/{uuid.uuid4().hex}.pdf"
    with open(path, "wb") as f:
        f.write(resp.content)
    return path

def ingest_pdf(file_obj=None, url: Optional[str] = None) -> Tuple[str, str]:
    """Ingest PDF from upload or URL; returns (local_path, source_name)."""
    if file_obj is not None:
        if not file_obj.name.lower().endswith(".pdf"):
            raise ValueError("Uploaded file is not a PDF.")
        return file_obj.name, os.path.basename(file_obj.name)

    if url and url.strip():
        local_path = download_pdf(url.strip())
        source_name = url.strip().split("/")[-1] or "downloaded.pdf"
        if not source_name.lower().endswith(".pdf"):
            source_name += ".pdf"
        return local_path, source_name

    raise ValueError("Please upload a PDF or provide a PDF URL.")
