import os
from dotenv import load_dotenv

# .env 파일이 있으면 로드
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'aisci.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ollama / LLM
    LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "mock")  # mock | ollama
    OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1")
    OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")

    # Generated projects
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "generated_projects")
