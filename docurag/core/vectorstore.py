import os
import shutil
import tempfile
from dataclasses import dataclass

import chromadb
from chromadb.utils import embedding_functions

@dataclass
class VectorStore:
    client: chromadb.PersistentClient
    collection: any
    session_dir: str

def create_vector_store(openai_api_key: str, embedding_model: str) -> VectorStore:
    """Create Chroma in a unique temp directory per session."""
    session_dir = tempfile.mkdtemp(prefix="chroma_session_")
    client = chromadb.PersistentClient(path=session_dir)
    emb_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_api_key,
        model_name=embedding_model
    )
    collection = client.get_or_create_collection(
        name="pdf_rag_collection",
        embedding_function=emb_fn
    )
    return VectorStore(client=client, collection=collection, session_dir=session_dir)

def reset_vector_store(vs: VectorStore, openai_api_key: str, embedding_model: str) -> VectorStore:
    """Delete prior session dir and create a new store."""
    try:
        if vs and vs.session_dir and os.path.exists(vs.session_dir):
            shutil.rmtree(vs.session_dir, ignore_errors=True)
    except Exception:
        pass
    return create_vector_store(openai_api_key, embedding_model)
