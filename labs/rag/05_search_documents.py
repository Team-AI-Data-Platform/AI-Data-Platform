"""
Step2-3. RAG 질의응답 구현 - 05_search_documents.py

역할:
- 사용자의 질문을 Chroma Vector DB에 질의한다.
- 질문과 의미적으로 유사한 문서 조각을 검색한다.

실행 예시:
    python labs/rag/05_search_documents.py
"""

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions


# 프로젝트 루트 기준 경로
BASE_DIR = Path(__file__).resolve().parent
CHROMA_DB_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "microserver_docs"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def get_collection():
    """Chroma DB 컬렉션을 가져온다."""
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )

    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )

    return collection


def search_documents(query: str, top_k: int = 3):
    """질문과 유사한 문서를 Vector DB에서 검색한다."""
    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    searched_docs = []

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


if __name__ == "__main__":
    user_query = "MicroServer 프레임워크의 주요 구성요소는 무엇인가?"

    print("사용자 질문:")
    print(user_query)
    print("\n검색 결과:")

    docs = search_documents(user_query, top_k=3)

    for doc in docs:
        print("=" * 80)
        print(f"순위: {doc['rank']}")
        print(f"거리: {doc['distance']}")
        print(f"메타데이터: {doc['metadata']}")
        print("문서 내용:")
        print(doc["document"])
