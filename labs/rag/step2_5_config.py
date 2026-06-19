"""
Step2-5A 실습 공통 설정 파일

모든 실습 스크립트는 이 파일의 경로와 설정값을 공통으로 사용한다.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

ENTERPRISE_DOCS_DIR = BASE_DIR / "enterprise_docs"
EXTRACTED_TEXT_DIR = BASE_DIR / "extracted_text"
CHUNKS_DIR = BASE_DIR / "enterprise_chunks"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "enterprise_docs"

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL_NAME = "llama3.1:8b"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
SEARCH_TOP_K = 5


def ensure_directories() -> None:
    """실습에 필요한 디렉터리를 생성한다."""
    EXTRACTED_TEXT_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

    for sub_dir in ["pdf", "pptx", "docx", "xlsx", "md", "txt"]:
        (ENTERPRISE_DOCS_DIR / sub_dir).mkdir(parents=True, exist_ok=True)
