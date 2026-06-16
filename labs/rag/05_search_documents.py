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


# 타입 힌트를 지연 평가(Lazy Evaluation)하여
# 순환 참조 및 자기 자신(Self Reference) 타입 선언을 가능하게 함
from __future__ import annotations

# 다양한 타입(str, int, list, dict 등)을 허용하는 범용 타입 힌트
# 주로 JSON, API 응답, Metadata 처리 시 사용
from typing import Any

# 파일 및 디렉터리 경로를 객체 형태로 다루기 위한 표준 라이브러리
from pathlib import Path


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


    # __file__ : 현재 실행 중인 Python 파일 경로(Python이 자동으로 제공하는 특수 변수이다.)
    # resolve() : 절대 경로로 변환
    # parent : 파일이 포함된 디렉터리 추출
    # 예) /labs/rag/05_search_documents.py -> /labs/rag
    script_dir = Path(__file__).resolve().parent
    print(f"script_dir : {script_dir}")

    # 현재 터미널에서 실행 중인 작업 디렉터리
    # (Current Working Directory)
    # 현재 터미널이 위치한 작업 디렉터리(CWD)를 가져온다.
    current_dir = Path.cwd()



    # ChromaDB 데이터가 저장되어 있을 가능성이 있는 경로 후보 목록을 만든다.
    # 실행 위치가 달라져도 chroma_db 디렉터리를 찾을 수 있도록
    # 여러 위치를 후보로 등록한다.
    candidate_paths = [
        script_dir / "chroma_db",      # labs/rag/chroma_db
        current_dir / "chroma_db",     # 현재 실행 위치/chroma_db
        script_dir.parent / "chroma_db",
        script_dir.parent.parent / "chroma_db",
    ]


    # 후보 경로를 순서대로 확인한다.
    # path.exists() : 해당 경로가 실제로 존재하는지 확인
    # path.is_dir() : 해당 경로가 파일이 아니라 디렉터리인지 확인
    # 둘 다 만족하는 첫 번째 경로를 ChromaDB 경로로 사용한다.
    for path in candidate_paths:
        if path.exists() and path.is_dir():

            # 존재하는 chroma_db 디렉터리를 찾으면 즉시 반환한다.
            # return 이 실행되면 함수가 종료되므로 아래 예외 처리(raise)는 실행되지 않는다.
            return path


    # 위 후보 경로 중 어느 곳에서도 chroma_db 디렉터리를 찾지 못한 경우,
    # 확인했던 경로 목록을 에러 메시지에 표시하기 위해 문자열로 만든다.
    # 예)
    # - /Users/.../labs/rag/chroma_db
    # - /Users/.../AI-Data-Platform/chroma_db

    ######################################################
    # Python의 Generator Expression 문법
    ######################################################
    # Python은 Java와 다르게 "반복문"보다 "결과식"을 먼저 작성한다.
    # 형식:
    # 결과식 for 변수 in 컬렉션
    # 예)
    # f"- {path}" for path in candidate_paths
    # 위 코드는 candidate_paths를 하나씩 순회하면서
    # 각 path를 "- 경로명" 형태의 문자열로 변환한다.
    # Java로 생각하면 아래와 비슷하다.
    #
    # for (Path path : candidatePaths) {
    #     result.add("- " + path);
    # }
    #
    # 이후 join()이 생성된 문자열들을 줄바꿈(\n)으로 연결한다.
    checked_paths = "\n".join(f"- {path}" for path in candidate_paths)




    # ChromaDB 디렉터리를 찾지 못한 경우 예외(Exception)를 발생시킨다.
    # raise 는 Java의 throw 와 동일한 개념이다.
    # 현재 함수 실행을 즉시 중단하고 호출한 곳으로 오류를 전달한다.
    # FileNotFoundError 는 파일 또는 디렉터리를 찾지 못했을 때 사용하는
    # Python의 내장 예외 클래스이다.
    # checked_paths 에는 실제로 확인한 경로 목록이 저장되어 있으며,
    # 오류 발생 시 어떤 경로들을 검사했는지 사용자에게 알려준다.
    # 예)
    # ChromaDB 디렉터리를 찾을 수 없습니다.
    # 먼저 03_insert_to_chroma.py를 실행해서 문서를 ChromaDB에 적재해야 합니다.
    # 확인한 경로:
    # - /labs/rag/chroma_db
    # - /project/chroma_db
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
