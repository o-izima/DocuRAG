<<<<<<< HEAD
<<<<<<< HEAD
# DocuRAG — PDF RAG Assistant (No LangChain)

DocuRAG is a **LangChain-free** PDF Retrieval-Augmented Generation (RAG) application that ingests PDFs (upload or URL), extracts text (with optional OCR), chunks content, embeds into **Chroma**, retrieves top-k passages, and generates grounded answers using the **OpenAI** API — with **source citations**.

## Architecture

```mermaid
flowchart LR
  A[User: Upload PDF / URL] --> B[Ingestion]
  B --> C[Extraction Cascade]
  C -->|fitz| C1[PyMuPDF text]
  C -->|fallback| C2[pdfplumber text]
  C -->|fallback| C3[OCR: pytesseract (optional)]
  C --> D[Chunking]
  D --> D1[Sentence-preserving]
  D --> D2[Word-window w/ overlap]
  D --> E[Embeddings: OpenAI text-embedding-3-small]
  E --> F[Vector DB: Chroma]
  F --> G[Retriever: top-k]
  G --> H[LLM: OpenAI gpt-4o-mini]
  H --> I[Answer + Citations]
```

## Features
- Upload PDFs or provide a PDF URL
- Extraction cascade per page: **fitz → pdfplumber → OCR**
- Dual chunking strategies (**sentence** / **word**) + **auto**
- Summary intent detection expands retrieval context for “summarize / main contributions”
- Citations show **source + page + snippet**
- Retrieval debug panel to show top-k chunks
- Reset button clears UI + vector store (fresh Chroma session)

## Setup

### Local
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# set OPENAI_API_KEY in .env
python -m docurag.ui.gradio_app
```

### Docker
```bash
docker build -t docurag .
docker run -p 7860:7860 --env OPENAI_API_KEY=$OPENAI_API_KEY docurag
```

### Hugging Face Spaces (Gradio)
- Create a Gradio Space
- Add `OPENAI_API_KEY` as a Secret
- Push this repo
- App file: `docurag/ui/gradio_app.py`

## Test PDFs
- https://arxiv.org/pdf/1706.03762.pdf
- https://arxiv.org/pdf/2501.12948.pdf

## Notes on OCR
True OCR requires the system package `tesseract-ocr`. The Dockerfile installs it. Some hosted environments may require additional setup.

## License
MIT
=======
---
title: Docurag
emoji: 🐠
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
license: mit
short_description: Retrieval-Augmented Generation over PDFs and URLs with OCR s
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
>>>>>>> 83bfbc7 (initial commit)
=======
---
title: DocuRAG — PDF RAG (No LangChain)
emoji: 📄
colorFrom: blue
colorTo: gray
sdk: gradio
sdk_version: 4.30.0
app_file: docurag/ui/gradio_app.py
pinned: false
---

# DocuRAG — PDF RAG Assistant (No LangChain)

DocuRAG is a **LangChain-free** PDF Retrieval-Augmented Generation (RAG) application that ingests PDFs (upload or URL), extracts text (with optional OCR), chunks content, embeds into **Chroma**, retrieves top-k passages, and generates grounded answers using the **OpenAI** API — with **source citations**.

## Architecture

```mermaid
flowchart LR
  A[User: Upload PDF / URL] --> B[Ingestion]
  B --> C[Extraction Cascade]
  C -->|fitz| C1[PyMuPDF text]
  C -->|fallback| C2[pdfplumber text]
  C -->|fallback| C3[OCR: pytesseract (optional)]
  C --> D[Chunking]
  D --> D1[Sentence-preserving]
  D --> D2[Word-window w/ overlap]
  D --> E[Embeddings: OpenAI text-embedding-3-small]
  E --> F[Vector DB: Chroma]
  F --> G[Retriever: top-k]
  G --> H[LLM: OpenAI gpt-4o-mini]
  H --> I[Answer + Citations]
```

## Features
- Upload PDFs or provide a PDF URL
- Extraction cascade per page: **fitz → pdfplumber → OCR**
- Dual chunking strategies (**sentence** / **word**) + **auto**
- Summary intent detection expands retrieval context for “summarize / main contributions”
- Citations show **source + page + snippet**
- Retrieval debug panel to show top-k chunks
- Reset button clears UI + vector store (fresh Chroma session)

## Setup

### Local
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# set OPENAI_API_KEY in .env
python -m docurag.ui.gradio_app
```

### Docker
```bash
docker build -t docurag .
docker run -p 7860:7860 --env OPENAI_API_KEY=$OPENAI_API_KEY docurag
```

### Hugging Face Spaces (Gradio)
- Create a Gradio Space
- Add `OPENAI_API_KEY` as a Secret
- Push this repo
- App file: `docurag/ui/gradio_app.py`

## Test PDFs
- https://arxiv.org/pdf/1706.03762.pdf
- https://arxiv.org/pdf/2501.12948.pdf

## Notes on OCR
True OCR requires the system package `tesseract-ocr`. The Dockerfile installs it. Some hosted environments may require additional setup.

## License
MIT
>>>>>>> d19c1e0 (Initial commit: DocuRAG modularized RAG app)
