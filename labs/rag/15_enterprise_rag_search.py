"""
15_enterprise_rag_search.py

ChromaDB에서 관련 문서를 검색하고 Ollama를 사용해 RAG 답변을 생성한다.

입력:
- chroma_db/

실행:
python 15_enterprise_rag_search.py "전자금융 장애 대응 절차를 알려줘"
"""




# =============================================================================
# import 문
# =============================================================================
# import는 다른 모듈(Module)이나 라이브러리(Library)의 기능을 현재 파일에서 사용할 수 있도록 가져오는 파이썬 문법이다.
# 파이썬은 기능을 모듈 단위(.py 파일)로 관리하며,필요한 기능만 import 해서 사용한다.
# 예)
# import math              -> math 모듈 전체 사용
# from math import sqrt    -> sqrt 함수만 사용
# 대부분의 프로그램은 필요한 라이브러리를 import 하면서 시작한다.
# =============================================================================


# 앞으로 파이썬 버전이 변경되어도 최신 타입 힌트 문법을 사용할 수 있게 해준다.
# (예: list[str], dict[str, int] 등의 타입 힌트)
from __future__ import annotations


# 파이썬 인터프리터 및 실행 환경과 관련된 기능을 제공하는 표준 라이브러리.
#
# 주요 기능
# - 프로그램 종료(sys.exit())
# - 명령행 인자(sys.argv)
# - 파이썬 버전 확인(sys.version)
# - 표준 입력/출력 제어(sys.stdin, sys.stdout)
#
# 현재 코드에서는 오류 발생 시 프로그램을 종료하기 위해 사용된다.
import sys


# typing 모듈은 타입 힌트(Type Hint)를 작성하기 위한 표준 라이브러리이다.
#
# Any
# - 어떤 타입이든 허용한다.
# - 타입을 아직 명확히 지정하기 어려울 때 사용한다.
#
# 예)
# value: Any
#
# 문자열, 숫자, 리스트, 객체 등 어떤 값도 저장할 수 있다.
from typing import Any


# ChromaDB 벡터 데이터베이스 라이브러리.
#
# 역할
# - 문서를 벡터(Vector) 형태로 저장
# - 유사도 검색(Semantic Search)
# - Collection 생성 및 조회
# - RAG(Retrieval-Augmented Generation)의 검색 엔진 역할
#
# 현재 프로젝트에서는
# 문서 Chunk를 저장하고 검색하기 위해 사용한다.
import chromadb


# HTTP 통신을 위한 가장 많이 사용되는 외부 라이브러리.
#
# 역할
# - REST API 호출
# - GET / POST 요청
# - JSON 데이터 송수신
#
# 현재 프로젝트에서는
# Ollama API를 호출하여 LLM에게 질문을 보내기 위해 사용한다.
import requests


# SentenceTransformer 라이브러리.
#
# sentence-transformers 패키지에서 제공하는 클래스이다.
#
# 역할
# - 문장을 임베딩(Vector)으로 변환
# - 의미 기반 검색(Semantic Search)에 사용
#
# 예)
# "오늘 날씨 어때?"
#      ↓
# [0.123, -0.453, 0.882, ...]
#
# 이렇게 변환된 벡터를 ChromaDB에 저장하거나 검색에 사용한다.
from sentence_transformers import SentenceTransformer


# 프로젝트에서 사용하는 설정값들을 별도의 설정 파일(step2_5_config.py)에서 가져온다.
#
# 이렇게 설정을 분리하면
# - 코드 수정 없이 설정만 변경 가능
# - 유지보수가 쉬움
# - 여러 파일에서 동일한 설정을 공유 가능
#
# 가져오는 설정값
#
# CHROMA_DB_DIR
#   → ChromaDB가 저장되는 디렉터리
#
# COLLECTION_NAME
#   → 사용할 ChromaDB Collection 이름
#
# EMBEDDING_MODEL_NAME
#   → SentenceTransformer 모델명
#
# OLLAMA_BASE_URL
#   → Ollama 서버 주소
#
# OLLAMA_MODEL_NAME
#   → 사용할 LLM 모델명
#
# SEARCH_TOP_K
#   → 검색 시 반환할 문서 개수
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
        # f"..."
        # f-string(문자열 포매팅) 문법.
        # 문자열 안에 {변수명}을 작성하면 변수의 값이 자동으로 문자열에 삽입된다.
        # 예)
        # file_name = "guide.pdf"
        # f"파일={file_name}"
        # → "파일=guide.pdf"
        # Java의 String.format()이나
        # "파일=" + fileName 과 비슷한 역할을 한다.
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

    ########################################
    # join()
    ########################################
    # 문자열(String) 클래스에서 제공하는 메서드.
    # 기능
    # - 리스트, 튜플 등의 문자열 요소를 하나의 문자열로 연결한다.
    # 역할
    # - 각 문자열 사이에 현재 문자열(", ")을 구분자로 삽입하여
    #   하나의 문자열을 생성한다.
    # 문법
    # "구분자".join(반복가능객체)
    # 반환값
    # - 연결된 새로운 문자열(str)
    # 예)
    # parts = ["파일=test.pdf", "페이지=3", "Chunk=5"]
    # ", ".join(parts)
    # → "파일=test.pdf, 페이지=3, Chunk=5"
    # Java의 String.join(", ", list)와 거의 동일한 기능이다.
    # 문자열을 '+' 연산자로 반복해서 연결하는 것보다 성능이 좋아 파이썬에서 가장 많이 사용하는 문자열 연결 방법이다.
    return ", ".join(parts)








def search_documents(query: str, top_k: int = SEARCH_TOP_K) -> list[dict[str, Any]]:
    """
    사용자 질문과 의미적으로 유사한 문서 Chunk를 ChromaDB에서 검색한다.

    이 함수는 RAG 처리 흐름에서 "검색(Retrieval)" 단계에 해당한다.
    사용자의 질문을 임베딩 벡터로 변환한 뒤, ChromaDB에 저장된 문서 Chunk 벡터들과
    비교하여 의미적으로 가장 가까운 Chunk 목록을 반환한다.

    처리 순서:
    1. CHROMA_DB_DIR 경로에 저장된 ChromaDB PersistentClient를 생성한다.
    2. COLLECTION_NAME 이름의 컬렉션을 조회한다.
    3. 컬렉션이 없으면 RuntimeError를 발생시킨다.
    4. 컬렉션은 존재하지만 저장된 문서가 0건이면 RuntimeError를 발생시킨다.
    5. SentenceTransformer 모델을 로딩한다.
    6. 사용자 질문(query)을 임베딩 벡터로 변환한다.
    7. ChromaDB에서 질문 벡터와 유사한 문서 Chunk를 top_k 개수만큼 검색한다.
    8. 검색 결과에서 문서 본문, 메타데이터, 거리값을 꺼낸다.
    9. 각 검색 결과에 순위(rank)를 붙여 리스트 형태로 반환한다.

    파라미터:
        query:
            사용자가 입력한 질문 문자열이다.
            이 질문은 SentenceTransformer 모델을 통해 임베딩 벡터로 변환된다.

        top_k:
            검색 결과로 가져올 최대 Chunk 개수이다.
            값을 직접 넘기지 않으면 설정 파일의 SEARCH_TOP_K 값을 기본값으로 사용한다.

    반환값:
        list[dict[str, Any]]:
            검색된 Chunk 목록을 리스트로 반환한다.

            각 항목은 다음 구조를 가진다.

            {
                "rank": 검색 순위,
                "text": 검색된 Chunk 본문,
                "metadata": Chunk에 함께 저장된 메타데이터,
                "distance": 질문 벡터와 문서 Chunk 벡터 사이의 거리값
            }

            distance 값은 ChromaDB가 계산한 유사도 거리이다.
            일반적으로 distance가 작을수록 질문과 문서 Chunk가 더 유사하다고 볼 수 있다.

    예외:
        RuntimeError:
            - ChromaDB 컬렉션을 찾을 수 없는 경우
            - 컬렉션은 존재하지만 저장된 문서가 없는 경우

    참고:
        이 함수는 LLM에게 바로 질문하지 않는다.
        역할은 질문과 관련 있는 근거 문서 Chunk를 찾는 것이다.
        이후 단계에서 검색된 Chunk들을 프롬프트에 포함하여 Ollama LLM에 전달하면
        RAG 기반 답변을 생성할 수 있다.
    """




    # ChromaDB PersistentClient를 생성한다.
    # CHROMA_DB_DIR 경로에 저장된 ChromaDB(벡터DB)에 연결하기 위한 객체를 생성한다.
    # 이후 Collection 조회, 문서 검색 등의 모든 작업은 이 client 객체를 통해 수행한다.
    client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))




    try:

        # 지정한 이름(COLLECTION_NAME)의 ChromaDB 컬렉션을 가져온다.
        # 컬렉션은 벡터 데이터와 메타데이터를 저장하는 저장소이며,
        # 이후 유사도 검색(query) 등의 작업은 collection 객체를 통해 수행한다.
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



    # SentenceTransformer 임베딩 모델을 로딩한다.
    # 사용자 질문을 벡터(Embedding)로 변환하기 위한 AI 모델 객체를 생성한다.
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # 사용자 질문(query)을 임베딩 벡터로 변환한다.
    # encode()는 여러 문장을 한 번에 임베딩할 수 있도록 설계된 함수이므로,
    # 질문이 1개뿐이어도 리스트([query]) 형태로 전달한다.
    # 반환값도 2차원 배열이므로 tolist()[0]으로 첫 번째 벡터만 추출한다.
    query_embedding = model.encode([query]).tolist()[0]




    # ChromaDB에서 질문 벡터와 가장 유사한 문서 Chunk를 검색한다.
    # query_embeddings는 검색 기준이 되는 질문 벡터이다.
    # 여러 질문을 한 번에 검색할 수 있도록 설계된 파라미터이므로,
    # 질문이 1개뿐이어도 리스트([query_embedding]) 형태로 전달한다.
    #
    # n_results
    # - 반환할 최대 검색 결과(Top-K) 개수
    #
    # include
    # - 검색 결과에 함께 반환할 데이터
    #   documents : 문서 Chunk 본문
    #   metadatas : 문서 메타데이터
    #   distances : 질문 벡터와 문서 벡터 사이의 거리(유사도)
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )




    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]




    



    ########################################
    # zip()
    ########################################
    # 파이썬 내장 함수(Built-in Function).
    # 기능
    # - 여러 개의 반복 가능한 객체(List, Tuple 등)를 같은 인덱스끼리 묶어준다.
    # 역할
    # - 여러 리스트를 동시에 순회할 수 있도록 하나의 반복 객체를 생성한다.
    # 문법
    # zip(iterable1, iterable2, ...)
    # 반환값
    # - zip 객체(Iterator)
    # 예)
    # names = ["Kim", "Lee"]
    # ages = [20, 30]
    # zip(names, ages)
    # → ("Kim", 20), ("Lee", 30)
    # 참고
    # - 전달된 리스트들의 길이가 서로 다르면
    #   가장 짧은 리스트의 길이까지만 묶어서 반환한다.
    # - Java에서는 여러 컬렉션을 동시에 순회하는 기능이 없어
    #   보통 동일한 인덱스를 이용하여 직접 반복문을 작성해야 한다.
    ########################################
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

    # 검색된 문서(Chunk) 목록을 순회하며 LLM에게 전달할 Context를 생성한다.
    for hit in hits:
        # 문서의 메타데이터를 사람이 읽기 쉬운 출처 문자열로 변환한다.
        source = format_source(hit["metadata"])

        # 검색된 문서의 순위, 출처, 내용을 하나의 문자열로 구성하여
        # Context 목록(context_lines)에 추가한다.
        # 이후 모든 Context를 하나로 합쳐 LLM의 프롬프트에 포함하여 전달한다.
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
    """
    RAG(Retrieval-Augmented Generation) 검색 및 질의응답 전체 과정을 실행한다.

    이 함수는 프로그램의 시작점(Entry Point)으로,
    사용자의 질문을 입력받아 문서를 검색하고, 검색된 결과를 기반으로
    Ollama LLM에게 질문하여 최종 답변을 생성하고 출력한다.

    처리 순서:
    1. 명령행 인자(sys.argv)에 질문이 전달되었는지 확인한다.
       - 전달된 경우 : 명령행 인자를 질문으로 사용한다.
       - 전달되지 않은 경우 : input()으로 사용자에게 질문을 입력받는다.
    2. 입력된 질문이 비어 있는지 검증한다.
    3. ChromaDB에서 질문과 의미적으로 유사한 문서 Chunk를 검색한다.
    4. 검색된 문서 목록을 화면에 출력한다.
    5. 검색 결과를 기반으로 RAG 프롬프트(Context)를 생성한다.
    6. 생성된 프롬프트를 Ollama LLM에 전달하여 답변을 생성한다.
    7. 생성된 답변을 화면에 출력한다.
    8. Ollama 서버가 실행 중이 아니거나 모델 호출에 실패한 경우
       오류 메시지와 실행 방법을 안내한다.

    참고:
        이 함수는 프로그램의 전체 실행 흐름만 제어하며,
        실제 검색(search_documents), 프롬프트 생성(build_prompt),
        LLM 호출(ask_ollama) 등의 세부 기능은 각각의 함수가 담당한다.
        즉, main()은 각 기능을 순서대로 호출하는 오케스트레이션(Orchestration) 역할을 수행한다.

    반환값:
        없음(None)
    """



    # 프로그램 실행 시 명령행 인자로 질문이 전달되었는지 확인한다.
    # 예)
    # python 15_enterprise_rag.py "RAG가 무엇인가?"
    if len(sys.argv) >= 2:
        # 프로그램명(sys.argv[0])을 제외한 나머지 인자를 하나의 문자열로 합친다.
        #
        # sys.argv 구조
        # sys.argv[0] : 실행한 파이썬 파일명
        # sys.argv[1:] : 사용자가 입력한 명령행 인자 목록
        #
        # 예)
        # python 15_enterprise_rag.py RAG 는 무엇인가?
        #
        # sys.argv
        # [
        #     "15_enterprise_rag.py",
        #     "RAG",
        #     "는",
        #     "무엇인가?"
        # ]
        #
        # " ".join(sys.argv[1:])
        # → "RAG 는 무엇인가?"
        #
        # 마지막으로 strip()을 호출하여 앞뒤 공백을 제거한다.
        query = " ".join(sys.argv[1:]).strip()
        #파이썬의 슬라이싱(Slicing) 문법 
        # 리스트[시작인덱스:끝인덱스]
        # [1:] --> 1번 인덱스부터 마지막까지 가져와라

    else:
        # 명령행 인자가 없으면 사용자에게 질문을 입력받는다.
        # input()은 콘솔에서 입력받은 문자열을 반환하며,
        # strip()을 호출하여 입력값의 앞뒤 공백을 제거한다.
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
