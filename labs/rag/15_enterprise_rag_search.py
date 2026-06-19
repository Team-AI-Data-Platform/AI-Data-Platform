"""
15_enterprise_rag_search.py

ChromaDB에서 관련 문서를 검색하고 Ollama를 사용해 RAG 답변을 생성한다.

입력:
- chroma_db/

실행:
python 15_enterprise_rag_search.py "전자금융 장애 대응 절차를 알려줘"
"""

from __future__ import annotations

import sys
from typing import Any

import chromadb
import requests
from sentence_transformers import SentenceTransformer

from step2_5_config import (
    CHROMA_DB_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL_NAME,
    SEARCH_TOP_K,
)


def format_source(metadata: dict[str, Any]) -> str:
    """검색 결과의 출처 정보를 사람이 읽기 좋게 구성한다."""
    parts = []

    file_name = metadata.get("file_name")
    if file_name:
        parts.append(f"파일={file_name}")

    document_type = metadata.get("document_type")
    if document_type:
        parts.append(f"유형={document_type}")

    if metadata.get("page_no"):
        parts.append(f"페이지={metadata.get('page_no')}")

    if metadata.get("slide_no"):
        parts.append(f"슬라이드={metadata.get('slide_no')}")

    if metadata.get("sheet_name"):
        parts.append(f"시트={metadata.get('sheet_name')}")

    if metadata.get("row_no"):
        parts.append(f"행={metadata.get('row_no')}")

    if metadata.get("section"):
        parts.append(f"섹션={metadata.get('section')}")

    if metadata.get("chunk_index"):
        parts.append(f"Chunk={metadata.get('chunk_index')}")

    return ", ".join(parts)


def search_documents(query: str, top_k: int = SEARCH_TOP_K) -> list[dict[str, Any]]:
    """질문과 유사한 Chunk를 ChromaDB에서 검색한다."""
    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as exc:
        raise RuntimeError(
            f"ChromaDB 컬렉션을 찾을 수 없습니다: {COLLECTION_NAME}\n"
            "먼저 14_insert_enterprise_docs_to_chroma.py를 실행하세요."
        ) from exc

    if collection.count() == 0:
        raise RuntimeError(
            f"ChromaDB 컬렉션은 존재하지만 저장된 문서가 없습니다: {COLLECTION_NAME}"
        )

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    query_embedding = model.encode([query]).tolist()[0]

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    hits: list[dict[str, Any]] = []

    for rank, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):
        hits.append(
            {
                "rank": rank,
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return hits


def build_prompt(query: str, hits: list[dict[str, Any]]) -> str:
    """LLM에 전달할 RAG Prompt를 생성한다."""
    context_lines = []

    for hit in hits:
        source = format_source(hit["metadata"])
        context_lines.append(
            f"[문서 {hit['rank']}]\n"
            f"출처: {source}\n"
            f"내용:\n{hit['text']}"
        )

    context = "\n\n".join(context_lines)

    return f"""너는 사내 문서 기반 RAG 답변 도우미이다.

아래 [참고 문서]만 근거로 사용해서 질문에 답변하라.
참고 문서에 없는 내용은 추측하지 말고 "제공된 문서에서는 확인되지 않습니다."라고 답변하라.
답변 마지막에는 사용한 출처를 요약하라.

[참고 문서]
{context}

[질문]
{query}

[답변]
"""


def ask_ollama(prompt: str) -> str | None:
    """Ollama API로 답변을 생성한다. 실패하면 None을 반환한다."""
    url = f"{OLLAMA_BASE_URL}/api/generate"

    payload = {
        "model": OLLAMA_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
    except Exception as exc:
        print(f"[Ollama 호출 실패] {exc}")
        return None

    if response.status_code != 200:
        print(f"[Ollama 응답 오류] status={response.status_code}, body={response.text[:300]}")
        return None

    data = response.json()
    return data.get("response")


def print_search_results(hits: list[dict[str, Any]]) -> None:
    """검색 결과를 출력한다."""
    print("=" * 80)
    print("검색 결과")
    print("=" * 80)

    for hit in hits:
        print(f"[{hit['rank']}] distance={hit['distance']:.4f}")
        print(f"출처: {format_source(hit['metadata'])}")
        print("-" * 80)
        print(hit["text"][:700])
        print()


def main() -> None:
    if len(sys.argv) >= 2:
        query = " ".join(sys.argv[1:]).strip()
    else:
        query = input("질문을 입력하세요: ").strip()

    if not query:
        raise ValueError("질문이 비어 있습니다.")

    hits = search_documents(query)
    print_search_results(hits)

    prompt = build_prompt(query, hits)
    answer = ask_ollama(prompt)

    print("=" * 80)
    print("RAG 답변")
    print("=" * 80)

    if answer:
        print(answer.strip())
    else:
        print(
            "Ollama가 실행 중이 아니거나 모델 호출에 실패했습니다.\n"
            "검색 결과는 위에 출력되었습니다.\n\n"
            "Ollama 실행 예:\n"
            "ollama serve\n"
            "ollama pull llama3.1:8b"
        )


if __name__ == "__main__":
    main()
