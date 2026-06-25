"""
Step2-5A 실습 공통 설정 파일

모든 실습 스크립트는 이 파일의 경로와 설정값을 공통으로 사용한다.
"""

from pathlib import Path

#__file__ :: “현재 실행 중인 파이썬 파일 자신의 경로” 를 알려주는 파이썬 내장 특수 변수다.#
BASE_DIR = Path(__file__).resolve().parent

ENTERPRISE_DOCS_DIR = BASE_DIR / "enterprise_docs"
EXTRACTED_TEXT_DIR = BASE_DIR / "extracted_text"
CHUNKS_DIR = BASE_DIR / "enterprise_chunks"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "enterprise_docs"

EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL_NAME = "gemma3:4b"
#OLLAMA_MODEL_NAME = "llama3.1:8b"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
SEARCH_TOP_K = 5


def ensure_directories() -> None:
    """실습에 필요한 디렉터리를 생성한다."""
    #parents=True ==> 부모디렉토리 까지 자동 생성.
    #exist_ok=True ==> 이미 존재하면 그대로 사용
    EXTRACTED_TEXT_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

    for sub_dir in ["pdf", "pptx", "docx", "xlsx", "md", "txt"]:
        (ENTERPRISE_DOCS_DIR / sub_dir).mkdir(parents=True, exist_ok=True)
