import os
import gradio as gr
from openai import OpenAI

from docurag.core.config import load_settings
from docurag.core.ingestion import ingest_pdf
from docurag.core.vectorstore import create_vector_store, reset_vector_store
from docurag.core.rag import index_document, retrieve, generate_answer, is_summary_intent
from docurag.ui.formatting import format_sources, format_debug_retrieval
from docurag.utils.nlp import ensure_nltk_resources


def build_app():
    settings = load_settings()
    ensure_nltk_resources()

    client = OpenAI(api_key=settings.openai_api_key)
    vs = create_vector_store(settings.openai_api_key, settings.embedding_model)

    def clear_all():
        nonlocal vs
        vs = reset_vector_store(vs, settings.openai_api_key, settings.embedding_model)
        return "", "", "Ready.", None, "", "", "(Enable 'Show retrieval debug' to display retrieved chunks.)"

    def process_input(file, url, query, k, debug_mode, chunk_mode):
        nonlocal vs

        q = (query or "").strip()
        if not q:
            return "Error: Please type your question here.", "", "❌ Missing question.", ""

        status = "Using existing indexed document."

        # Re-index if new doc provided
        if file is not None or (url and url.strip()):
            vs = reset_vector_store(vs, settings.openai_api_key, settings.embedding_model)
            local_path, source_name = ingest_pdf(file_obj=file, url=url)
            status, _stats = index_document(vs.collection, local_path, source_name, chunk_mode=chunk_mode)

        eff_k = max(int(k), settings.summary_top_k) if is_summary_intent(q) else int(k)
        docs, metas = retrieve(vs.collection, q, k=eff_k)

        debug_text = format_debug_retrieval(docs, metas) if debug_mode else ""

        if not docs:
            status2 = status + " | Retrieval: 0 chunks"
            return "The provided context does not contain relevant information.", "No citations.", status2, debug_text

        answer, used_sources = generate_answer(client, q, docs, metas, chat_model=settings.chat_model)
        citations = format_sources(used_sources)
        return answer, citations, status, debug_text

    with gr.Blocks(theme=gr.themes.Soft(), title="DocuRAG — PDF RAG (No LangChain)") as demo:
        gr.Markdown(
            "# 📄 DocuRAG — PDF RAG Assistant (No LangChain)\n"
            "Upload a PDF or paste a PDF URL. Ask questions and get answers with **source + page** citations."
        )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📥 Document")
                file_input = gr.File(label="Upload PDF", file_types=[".pdf"])
                url_input = gr.Textbox(label="Or PDF URL", placeholder="https://arxiv.org/pdf/1706.03762.pdf")

                gr.Markdown("### ⚙️ Retrieval")
                k_slider = gr.Slider(2, 10, value=settings.default_top_k, step=1, label="Top-K chunks")
                debug_mode = gr.Checkbox(value=False, label="Show retrieval debug")

                gr.Markdown("### 🧩 Chunking")
                chunk_mode = gr.Dropdown(
                    choices=["auto", "sentence", "word"],
                    value=settings.chunk_mode_default,
                    label="Chunking strategy"
                )

                status_box = gr.Textbox(label="Status", value="Ready.", interactive=False)
                clear_btn = gr.Button("Clear / Reset session", variant="primary")

            with gr.Column():
                gr.Markdown("### 💬 Ask")
                query_input = gr.Textbox(
                    label="Type your question here",
                    placeholder="e.g., What is self-attention and why is it useful?",
                    lines=2
                )
                ask_btn = gr.Button("Ask", variant="primary")

                gr.Markdown("### ✅ Answer")
                answer_output = gr.Markdown()

                gr.Markdown("### 📚 Citations")
                sources_output = gr.Markdown()

                with gr.Accordion("🧪 Retrieval Debug (Top-K chunks)", open=False):
                    debug_output = gr.Markdown(value="(Enable 'Show retrieval debug' to display retrieved chunks.)")

        ask_btn.click(
            process_input,
            inputs=[file_input, url_input, query_input, k_slider, debug_mode, chunk_mode],
            outputs=[answer_output, sources_output, status_box, debug_output]
        )

        clear_btn.click(
            clear_all,
            outputs=[answer_output, sources_output, status_box, file_input, url_input, query_input, debug_output]
        )

    return demo


if __name__ == "__main__":
    app = build_app()
    on_spaces = os.getenv("SPACE_ID") is not None

    app.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", "7860")),
        share=not on_spaces,
    )
