import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Load and expose environment settings for the application."""

    def __init__(self) -> None:
        """Initialize settings from environment variables."""
        # 1. Project information
        self.ENV: str = os.getenv("ENV", "dev")
        self.API_BASE_URL: str = os.getenv("API_BASE_URL", "")

        # 2. API configuration
        self.BASE_PATH: str = os.getenv("BASE_PATH", "")
        self.OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY", None)
        self.GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY", None)
        self.OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
        self.GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY", None)

settings = Settings()