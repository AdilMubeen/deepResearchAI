"""Application configuration and environment setup."""
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class Config:
    # API credentials
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION", "2024-12-01-preview")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

    # Research parameters
    MAX_SEARCH_DEPTH = int(os.getenv("MAX_SEARCH_DEPTH", "5"))
    MAX_QUERIES_PER_SEARCH = int(os.getenv("MAX_QUERIES_PER_SEARCH", "8"))
    MAX_RESULTS_PER_QUERY = int(os.getenv("MAX_RESULTS_PER_QUERY", "5"))
    DEFAULT_BUDGET = float(os.getenv("DEFAULT_BUDGET", "20.0"))

    # Output paths
    OUTPUT_DIR = Path("outputs")
    REPORTS_DIR = OUTPUT_DIR / "reports"
    LOGS_DIR = OUTPUT_DIR / "logs"

    @classmethod
    def validate(cls):
        """Ensure all required API keys are configured."""
        required = {
            "AZURE_OPENAI_KEY": cls.AZURE_OPENAI_KEY,
            "AZURE_OPENAI_ENDPOINT": cls.AZURE_OPENAI_ENDPOINT,
            "ANTHROPIC_API_KEY": cls.ANTHROPIC_API_KEY,
            "GEMINI_API_KEY": cls.GEMINI_API_KEY,
            "PERPLEXITY_API_KEY": cls.PERPLEXITY_API_KEY,
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")

    @classmethod
    def setup_directories(cls):
        """Create output directories if they don't exist."""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.REPORTS_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)


Config.validate()
Config.setup_directories()
