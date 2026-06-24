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
    # 실습에 필요한 디렉터리 생성
    ensure_directories()

    # 13번 실습에서 생성한 Chunk 데이터(JSONL) 경로
    chunk_path = CHUNKS_DIR / "enterprise_chunks.jsonl"

    # JSONL 파일을 읽어 Chunk 목록(list[dict]) 로드
    records = read_jsonl(chunk_path)

    # Chunk 데이터가 없으면 실습 중단
    if not records:
        raise RuntimeError(
            f"Chunk 데이터가 없습니다: {chunk_path}\n"
            "먼저 13_build_enterprise_chunks.py를 실행하세요."
        )

    print("=" * 80)
    print("Embedding 모델 로딩")
    print("-" * 80)
    print(EMBEDDING_MODEL_NAME)

    # 문장을 벡터(Embedding)로 변환할 모델 로드
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # ChromaDB 저장에 필요한 데이터 분리
    #
    # ids        : Chunk 고유 ID 목록
    # documents  : Chunk 텍스트 목록
    # metadatas  : Chunk 메타데이터 목록
    ids = [record["id"] for record in records]
    documents = [record["text"] for record in records]
    metadatas = [record["metadata"] for record in records]

    print("=" * 80)
    print("Embedding 생성")
    print("-" * 80)
    print(f"Chunk 수: {len(documents)}")

    # Chunk 텍스트를 벡터(List[float])로 변환
    #
    # 결과 예시:
    # [
    #   [0.123, -0.456, ...],
    #   [0.789,  0.111, ...]
    # ]
    embeddings = model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    # 로컬 ChromaDB 연결
    client = chromadb.PersistentClient(
        path=str(CHROMA_DB_DIR)
    )

    # 실습에서는 매번 같은 결과를 확인하기 위해
    # 기존 컬렉션을 삭제 후 재생성한다.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    # 문서를 저장할 컬렉션 생성
    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    # ChromaDB 저장
    #
    # ids        : Chunk 고유 ID
    # documents  : Chunk 원문
    # metadatas  : 문서 정보
    # embeddings : 벡터 데이터
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
