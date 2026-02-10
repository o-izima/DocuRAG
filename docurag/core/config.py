import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"
    default_top_k: int = 6
    summary_top_k: int = 10
    chunk_mode_default: str = "auto"  # auto | sentence | word

def load_settings() -> Settings:
    """Load environment variables and return Settings.

    In Hugging Face Spaces, set OPENAI_API_KEY in Secrets.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    return Settings(openai_api_key=api_key)
