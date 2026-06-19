"""
14_insert_enterprise_docs_to_chroma.py

Chunk를 Embedding하여 ChromaDB에 저장한다.

입력:
- enterprise_chunks/enterprise_chunks.jsonl

출력:
- chroma_db/

실행:
python 14_insert_enterprise_docs_to_chroma.py
"""

from __future__ import annotations

import chromadb
from sentence_transformers import SentenceTransformer

from step2_5_config import (
    CHROMA_DB_DIR,
    CHUNKS_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    ensure_directories,
)
from step2_5_utils import read_jsonl


def main() -> None:
    ensure_directories()

    chunk_path = CHUNKS_DIR / "enterprise_chunks.jsonl"
    records = read_jsonl(chunk_path)

    if not records:
        raise RuntimeError(
            f"Chunk 데이터가 없습니다: {chunk_path}\n"
            "먼저 13_build_enterprise_chunks.py를 실행하세요."
        )

    print("=" * 80)
    print("Embedding 모델 로딩")
    print("-" * 80)
    print(EMBEDDING_MODEL_NAME)

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    ids = [record["id"] for record in records]
    documents = [record["text"] for record in records]
    metadatas = [record["metadata"] for record in records]

    print("=" * 80)
    print("Embedding 생성")
    print("-" * 80)
    print(f"Chunk 수: {len(documents)}")

    embeddings = model.encode(documents, show_progress_bar=True).tolist()

    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))

    # 실습에서는 매번 같은 결과를 확인하기 위해 기존 컬렉션을 삭제 후 재생성한다.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print("=" * 80)
    print("ChromaDB 저장 완료")
    print("-" * 80)
    print(f"컬렉션명: {COLLECTION_NAME}")
    print(f"저장 건수: {collection.count()}")
    print(f"저장 경로: {CHROMA_DB_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()
