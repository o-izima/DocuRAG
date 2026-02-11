---
title: DocuRAG - Document PDF RAG with OCR (No LangChain)
emoji: 📄
colorFrom: blue
colorTo: gray
sdk: gradio
sdk_version: "6.5.1"
app_file: docurag/ui/gradio_app.py
pinned: false
---

<a name="top"></a>
# 📄 DocuRAG — Document Retrieval‑Augmented Generation (RAG)

DocuRAG is a **production‑style, modular Retrieval‑Augmented Generation (RAG) system** designed to demonstrate how modern LLM applications retrieve, ground, and generate answers over **user‑supplied documents** — *without LangChain*.

It is built to showcase **applied ML, NLP, and systems design skills** relevant to real‑world RAG deployments.

---

## 🚀 Project Overview

DocuRAG enables users to ask natural‑language questions over custom knowledge sources provided via:

- 📂 **Local PDF upload**
- 🌐 **URL ingestion** (automatic fetch + processing)

The system retrieves the most relevant document segments using **vector similarity search (Chroma)** and generates **context‑grounded answers** using an LLM, with optional **summary‑style responses** when intent is detected.

Key design goals:
- Clear separation of concerns
- Extensibility across models and embeddings
- Robust document ingestion (including OCR)
- Session‑isolated retrieval to avoid data leakage

---


## 🏗️ Architecture Overview

```mermaid
flowchart TD
  A[Gradio UI] --> B[Ingestion]
  B -->|PDF| C[Extraction Cascade]
  B -->|URL| D[URL Fetch]
  C --> E[Text Cleaning]
  D --> E
  E --> F[Chunking]
  F --> G[Chroma Vector Store]
  H[User Query] --> I[RAG Orchestrator]
  I --> G
  G --> I
  I --> K[LLM Generation]
  K --> A
```

---

## 🧩 Codebase Structure

```text
docurag/
├─ docurag/
│  ├─ core/
│  │  ├─ config.py        # environment + settings
│  │  ├─ ingestion.py     # PDF / URL ingestion
│  │  ├─ extraction.py    # fitz → pdfplumber → OCR cascade
│  │  ├─ chunking.py      # word / sentence / auto
│  │  ├─ vectorstore.py   # per‑session Chroma
│  │  └─ rag.py           # indexing, retrieval, generation
│  ├─ ui/
│  │  ├─ formatting.py    # citations + debug output
│  │  └─ gradio_app.py    # Gradio UI
│  └─ utils/
│     ├─ text.py          # text cleaning
│     └─ nlp.py           # NLTK helpers
├─ app.py                 # HF Spaces entry point
├─ Dockerfile             # includes tesseract‑ocr
├─ requirements.txt
├─ pyproject.toml
├─ .env.example
└─ README.md
```

---


## ✨ Core Functionalities (What This System Demonstrates)

This project intentionally mirrors decisions made in real applied‑AI systems.

### 📄 Document Ingestion
- Upload **native or scanned PDFs**
- Ingest **web content via URL**
- Metadata preservation for citations

### 🔍 Robust Text Extraction
- **Cascade extraction strategy**:
  1. PyMuPDF (`fitz`) — fast, native PDFs
  2. pdfplumber — complex layouts
  3. OCR fallback (Tesseract) — scanned documents

### ✂️ Intelligent Chunking
- Word‑window chunking with overlap
- Sentence‑based chunking (NLTK)
- **Auto mode** that adapts to document size

### 🧠 Retrieval‑Augmented Generation
- Session‑scoped **Chroma vector stores**
- Top‑K similarity retrieval
- Context‑bounded prompting
- **Summary‑intent detection** vs QA routing

### 🧾 Traceability & Citations
- Page‑level source attribution
- Optional debug traces
- Clean formatting for UI display

### 🖥️ Deployment‑Ready UI
- Gradio interface
- Local, Docker, and Hugging Face Spaces support

### 🐳 Docker & OCR Support (Tesseract)

DocuRAG implements a **robust document extraction cascade** (`docurag/core/extraction.py`):

**PyMuPDF (`fitz`) → pdfplumber → OCR fallback**

This design matters because **many real-world PDFs are scanned images**, not “true text” PDFs.  
When a document contains only images, standard text extraction returns little or nothing — so the system **automatically falls back to OCR**.

#### Why Tesseract is included in Docker

The provided `Dockerfile` installs **`tesseract-ocr`** to ensure:

- ✅ Reliable OCR in containerized deployments  
- ✅ Consistent behavior across OS environments  
- ✅ No “works on my machine” extraction failures  
- ✅ True document intelligence for scanned PDFs  

This is especially important for **production and Hugging Face Spaces deployments**.

---

## 🎯 Key Design Goals
- **Clear separation of concerns:**
Each stage of the RAG pipeline (ingestion, extraction, chunking, retrieval, generation, and UI) is isolated into well-defined modules, improving readability, testability, and long-term maintainability.

- **Robust document ingestion with OCR support:**
Documents are processed using a resilient extraction cascade (native PDF parsing → layout-aware extraction → OCR fallback), ensuring both digital and scanned PDFs are handled reliably.

- **Session-isolated retrieval to prevent data leakage:**
Each user session operates on its own vector store instance, preventing cross-document or cross-user contamination during retrieval and generation.

- **Extensibility across models and embedding providers:**
LLMs and embedding models are configured via environment settings, making it easy to swap providers or models without changing core logic.

- **Multiple ingestion paths (local files + URLs):**
Users can upload PDFs from their local machine or provide a URL, both routed through the same downstream processing and indexing pipeline.

- **Configurable chunking and retrieval strategies:**
Chunking mode (auto, sentence-based, or word-window) and retrieval depth (Top-K) are exposed as configurable parameters to support different document types and query behaviors.

- **Grounded generation with explicit source attribution:**
Answers are generated strictly from retrieved document context and returned with citations (source and page), reducing hallucination and improving transparency.

- **Docker-first deployment for reproducibility:**
The application is designed to run consistently across local environments, Hugging Face Spaces, and other platforms using Docker, including all system-level dependencies.

- **OCR-ready containerized runtime:**
The Docker image includes tesseract-ocr, ensuring OCR functionality works reliably in cloud and containerized deployments without additional setup.

- **Minimal framework coupling:**
The RAG pipeline is implemented without heavy orchestration frameworks, keeping the logic explicit, debuggable, and easy to reason about.

---

## ▶️ Running DocuRAG

### 🖥️ Run Locally (Recommended for Development)
#### Clone the Repository
```bash
git clone https://github.com/o-izima/DocuRAG.git
cd DocuRAG
```

### Create and Configure `.env`

```bash
cp .env.example .env
```

Edit `.env` and set at least:

```bash
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=your_llm_model_name
EMBEDDING_MODEL_NAME=your_embedding_model_name
```
Optional but recommended (tune retrieval behavior):

```bash
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K=5
```
You may also configure additional retrieval or chunking parameters depending on your use case.

#### Using `pip`
```bash

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .\.venv\Scripts\activate     # Windows PowerShell
pip install -r requirements.txt
```

Start the Gradio UI:

```bash
python -m docurag.ui.gradio_app
```

If your repository includes the helper script, you can also run:

```bash
bash scripts/run_gradio.sh

```
Then open:

```bash
http://localhost:7860
```

---

### 🐳 Run with Docker (Best for OCR Reliability)

```bash
docker build -t docurag .
docker run -p 7860:7860 --env-file .env docurag
```
Then open:

```bash
http://localhost:7860
```

✅ Docker is strongly recommended if you plan to ingest scanned PDFs, since tesseract-ocr is guaranteed to be available inside the container.

---

### 🤗 Run on Hugging Face Spaces

#### Typical Hugging Face Spaces Setup (Docker Space)

1. Create a new Space on Hugging Face  
2. Select **Docker** as the Space SDK  
3. Connect this repository *or* push the code directly  
4. Add environment variables in the Space settings:

```bash
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=your_llm_model_name
EMBEDDING_MODEL_NAME=your_embedding_model_name
TOP_K=5
CHUNK_SIZE=500
```

Hugging Face will:
- build the Docker image
- install dependencies (including OCR)
- host the Gradio app automatically

⚠️ If you rely on OCR in Spaces, Docker-based deployment is strongly recommended so that Tesseract is available at runtime.

---

## Quick testing PDFs

Use these in the URL field or download the files to your local computer:

- https://arxiv.org/pdf/1706.03762.pdf (Transformers)

- https://arxiv.org/pdf/2501.12948.pdf (DeepSeek-R1)

Try:

- “What is self-attention?”

- “Summarize the paper / main contributions”

---

## License

This project is licensed under the [MIT License](./LICENSE). See the LICENSE file for details.

[⬆ Go to Top](#top)

---

