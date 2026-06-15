"""
Step2-3. RAG 질의응답 구현 - 05_search_documents.py

역할:
- Step2-2의 03_insert_to_chroma.py에서 저장한 ChromaDB 컬렉션을 조회한다.
- 사용자의 질문을 03번 파일과 동일한 SentenceTransformer 모델로 임베딩한다.
- 질문 임베딩과 유사한 문서 Chunk를 ChromaDB에서 검색한다.

중요:
- 03_insert_to_chroma.py는 collection.add() 호출 시 embeddings를 직접 저장한다.
- 따라서 05_search_documents.py도 query_texts 방식보다 query_embeddings 방식으로 검색하는 것이 안전하다.
- ChromaDB 경로도 실행 위치에 따라 달라질 수 있으므로 여러 후보 경로를 확인한다.

실행 위치 권장:
    cd labs/rag
    python 05_search_documents.py

또는 프로젝트 루트에서:
    python labs/rag/05_search_documents.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer


# 03_insert_to_chroma.py와 반드시 동일해야 하는 설정값
COLLECTION_NAME = "microserver_docs"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def find_chroma_path() -> Path:
    """
    ChromaDB 저장 경로를 찾는다.

    03_insert_to_chroma.py에는 CHROMA_PATH = "chroma_db"로 되어 있다.
    이 값은 '명령을 실행한 현재 위치'를 기준으로 해석된다.

    예를 들어,
    1) cd labs/rag 후 python 03_insert_to_chroma.py 실행
       -> labs/rag/chroma_db 생성

    2) 프로젝트 루트에서 python labs/rag/03_insert_to_chroma.py 실행
       -> 프로젝트 루트/chroma_db 생성

    따라서 05번 파일에서는 자주 사용되는 후보 경로를 순서대로 확인한다.
    """
    script_dir = Path(__file__).resolve().parent
    current_dir = Path.cwd()

    candidate_paths = [
        script_dir / "chroma_db",      # labs/rag/chroma_db
        current_dir / "chroma_db",    # 현재 실행 위치/chroma_db
        script_dir.parent / "chroma_db",
        script_dir.parent.parent / "chroma_db",
    ]

    for path in candidate_paths:
        if path.exists() and path.is_dir():
            return path

    checked_paths = "\n".join(f"- {path}" for path in candidate_paths)

    raise FileNotFoundError(
        "ChromaDB 디렉터리를 찾을 수 없습니다.\n\n"
        "먼저 03_insert_to_chroma.py를 실행해서 문서를 ChromaDB에 적재해야 합니다.\n\n"
        "확인한 경로:\n"
        f"{checked_paths}"
    )


def get_collection(chroma_path: Path):
    """
    ChromaDB 컬렉션을 가져온다.

    여기서는 get_or_create_collection()이 아니라 get_collection()을 사용한다.
    이유는 Step2-3 검색 실습에서는 이미 03번에서 생성된 컬렉션이 있어야 하기 때문이다.

    만약 컬렉션이 없다면 새로 만들지 않고 오류를 발생시켜
    '03번 실습이 먼저 실행되지 않았다'는 사실을 명확하게 알 수 있게 한다.
    """
    client = chromadb.PersistentClient(path=str(chroma_path))

    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as exc:
        raise RuntimeError(
            f"ChromaDB에서 컬렉션을 찾을 수 없습니다: {COLLECTION_NAME}\n\n"
            "먼저 아래 순서로 Step2-2 실습을 실행했는지 확인하세요.\n"
            "1. python 01_create_sample_doc.py\n"
            "2. python 02_load_and_chunk.py\n"
            "3. python 03_insert_to_chroma.py\n\n"
            f"현재 ChromaDB 경로: {chroma_path}"
        ) from exc

    return collection


def search_documents(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """
    질문과 유사한 문서 Chunk를 검색한다.

    처리 순서:
    1. ChromaDB 경로 확인
    2. microserver_docs 컬렉션 조회
    3. 03번과 동일한 임베딩 모델 로딩
    4. 사용자 질문을 벡터로 변환
    5. ChromaDB에서 유사 문서 Top-K 검색
    """
    if not query or not query.strip():
        raise ValueError("검색 질문이 비어 있습니다.")

    chroma_path = find_chroma_path()
    collection = get_collection(chroma_path)

    total_count = collection.count()
    if total_count == 0:
        raise RuntimeError(
            f"컬렉션은 존재하지만 저장된 문서가 없습니다: {COLLECTION_NAME}\n"
            "03_insert_to_chroma.py 실행 결과를 다시 확인하세요."
        )

    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode([query]).tolist()

    n_results = min(top_k, total_count)

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    searched_docs: list[dict[str, Any]] = []

    for index, document in enumerate(documents):
        searched_docs.append(
            {
                "rank": index + 1,
                "document": document,
                "metadata": metadatas[index] if index < len(metadatas) else {},
                "distance": distances[index] if index < len(distances) else None,
            }
        )

    return searched_docs


def print_search_results(query: str, docs: list[dict[str, Any]]) -> None:
    """검색 결과를 실습자가 보기 쉬운 형태로 출력한다."""
    print("[사용자 질문]")
    print(query)

    print("\n[검색 결과]")
    if not docs:
        print("검색 결과가 없습니다.")
        return

    for doc in docs:
        print("=" * 80)
        print(f"순위: {doc['rank']}")
        print(f"거리: {doc['distance']}")
        print(f"메타데이터: {doc['metadata']}")
        print("-" * 80)
        print(doc["document"])


if __name__ == "__main__":
    user_query = "MicroServer 프레임워크의 주요 구성요소는 무엇인가?"

    results = search_documents(user_query, top_k=3)
    print_search_results(user_query, results)
