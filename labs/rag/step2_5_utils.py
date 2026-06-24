"""
Step2-5A 실습 공통 유틸리티

JSONL 저장, 텍스트 정제, Chunking, 파일 검색 등의 공통 함수를 제공한다.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable


def clean_text(text: str) -> str:
    """
    문서에서 추출한 텍스트를 RAG 적재에 적합하도록 정제한다.

    처리 내용:
    - Windows 줄바꿈을 Unix 줄바꿈으로 변환
    - 탭을 공백으로 변환
    - 여러 개의 공백을 하나로 축소
    - 빈 줄을 과도하게 줄임
    """
    if text is None:
        return ""

    text = str(text).replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\t", " ")
    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def stable_id(*parts: Any) -> str:
    """
    입력값을 조합하여 항상 동일한 고유 ID를 생성한다.

    동일한 입력값이 들어오면 항상 동일한 ID가 생성되며,다른 입력값이 들어오면 다른 ID가 생성된다.

    주로 문서 ID, Chunk ID 등 Vector DB에 저장할 고유 식별자(Primary Key) 생성에 사용한다.

    처리 방식:
        1. 입력값(parts)을 문자열로 변환
        2. "|" 구분자로 하나의 문자열 생성
        3. SHA1 해시값 생성
        4. 40자리 Hex 문자열 반환
    예시:
        stable_id("guide.pdf", "pdf")
        ↓
        "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3"
    참고:
        Python의 hash() 함수는 실행 시마다 결과가 달라질 수 있으므로 영구 저장용 ID로 사용하기 어렵다.
        이 함수는 SHA1 해시를 사용하여 프로그램을 재실행해도 동일한 ID를 보장한다.
    """
    raw = "|".join(str(part) for part in parts)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()




def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> int:
    """
    문서 목록을 JSONL 파일로 저장한다.

    JSONL(JSON Lines)은 한 줄에 하나의 JSON 객체를 저장하는 형식이다.

    이 함수는 전달받은 records 데이터를 순회하면서
    각 dict 객체를 JSON 문자열로 변환한 후
    한 줄씩 파일에 기록한다.

    저장 방식:
        - 파일이 없으면 새로 생성
        - 파일이 이미 존재하면 기존 내용을 모두 삭제하고
          새로 작성(Overwrite)

    예시:

        입력 데이터:

        [
            {"id": "1", "text": "문서1"},
            {"id": "2", "text": "문서2"}
        ]

        저장 결과:

        {"id":"1","text":"문서1"}
        {"id":"2","text":"문서2"}

    파라미터:
        path:
            저장할 JSONL 파일 경로

        records:
            저장할 문서 목록
            (Iterable[dict[str, Any]])

    리턴값:
        int
            저장된 JSON 객체 수

    참고:
        Append(추가 저장) 방식이 아니라
        Overwrite(전체 덮어쓰기) 방식이다.

        Append 방식으로 저장하려면
        path.open("a") 모드를 사용해야 한다.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0


    # JSONL 파일을 쓰기(write) 모드로 연다.
    # with:
    #   파일 사용이 끝나면 자동으로 close() 수행
    #   (예외 발생 시에도 자동 종료)
    # "w":
    #   Write 모드
    #   - 파일이 없으면 새로 생성
    #   - 파일이 있으면 기존 내용 삭제 후 새로 작성
    # encoding="utf-8":
    #   한글이 깨지지 않도록 UTF-8 인코딩 사용
    # as f:
    #   열린 파일 객체를 f 변수로 참조
    with path.open("w", encoding="utf-8") as f:
        for record in records:

            # dict 객체(record)를 JSON 문자열로 변환한 후 줄바꿈(\n)을 추가하여 JSONL 형식으로 저장한다.
            # ensure_ascii=False:
            #   한글을 \uXXXX 형태가 아닌 실제 한글로 저장
            # "\n":
            #   JSONL 규격에 맞게 한 줄에 JSON 객체 1개 저장
            # 예)
            #   {"id":"1","text":"문서1"}
            #   {"id":"2","text":"문서2"}
            # write():
            #   생성된 문자열을 파일에 기록
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

            ##############################
            # json.dumps()
            ##############################
            # 기능:
            #   Python 객체(dict, list 등)를 JSON 문자열(String)로 변환한다.
            #
            # 역할:
            #   파일 저장 또는 네트워크 전송이 가능하도록
            #   Python 객체를 JSON 형식으로 직렬화(Serialize)한다.
            #
            # 파라미터:
            #   record
            #     - JSON으로 변환할 Python 객체
            #
            #   ensure_ascii=False
            #     - 한글을 유니코드(\uXXXX)로 변환하지 않고
            #       실제 한글로 저장한다.
            #
            # 리턴값:
            #   str
            #     - JSON 형식 문자열
            #
            # 예)
            #
            # 입력:
            #   {
            #       "id": "1",
            #       "text": "문서1"
            #   }
            #
            # 결과:
            #   '{"id":"1","text":"문서1"}'
            #
            # 참고:
            #   json.loads()
            #     JSON 문자열 → Python 객체
            #
            #   json.dumps()
            #     Python 객체 → JSON 문자열
            ##############################

            count += 1

    return count






def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """
    JSONL 파일을 읽어 Python dict 목록으로 반환한다.

    JSONL은 한 줄에 하나의 JSON 객체가 저장된 파일 형식이다.
    이 함수는 파일을 한 줄씩 읽고, 각 줄을 json.loads()로 파싱하여
    Python dict 객체로 변환한 뒤 records 리스트에 담아 반환한다.

    파일이 존재하지 않으면 오류를 발생시키지 않고 빈 리스트를 반환한다.

    파라미터:
        path:
            읽을 JSONL 파일 경로

    리턴값:
        list[dict[str, Any]]:
            JSONL 각 줄을 dict로 변환한 문서 목록
    """
    if not path.exists():
        return []

    records: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    return records


def find_files(directory: Path, extensions: tuple[str, ...]) -> list[Path]:
    """지정된 디렉터리에서 확장자에 맞는 파일을 재귀적으로 찾는다."""
    if not directory.exists():
        return []

    results: list[Path] = []


    ##############################################################
    #제너레이터 표현식
    ##############################################################
    #(ext.lower() for ext in extensions)를
    # Generator Expression(제너레이터 표현식) 이라고 한다.
    ### cf) 함수의 유일한 인자로 제너레이터를 넘길 때는 바깥 괄호를 생략할 수 있다.

    # 파이썬 에서는 [x.lower() for x in extensions] 게 하면 리스트가 만들어지고
    # (x.lower() for x in extensions) 게 쓰면 제너레이터가 만들어 진다.
    #   tuple(...)  ::   tuple() 함수가 값을 하나씩 꺼냄  -->   튜플로 변환
    lower_extensions = tuple(ext.lower() for ext in extensions)




    ##############################################################
    # pathlib.Path.rglob()
    ##############################################################
    # 현재 디렉토리부터 시작해서 하위 폴더를 전부 재귀적으로 탐색하면서 파일을 찾는다.
    # 
    # cf) glob() 와 차이 :: 현재 폴더만 검색
    for path in directory.rglob("*"):
        
        # path.suffix :: Path 객체가 제공하는 속성(property)
        # -->파일의 확장자를 반환한다.
        # in 연산자 :: in 연산자는 어떤 값이 컬렉션(list, tuple, set, dict 등) 안에 포함되어 있는지 검사하는 연산자이다.
        if path.is_file() and path.suffix.lower() in lower_extensions:
            results.append(path)

    return sorted(results)
    ############################################################
    # Python 내장 함수 sorted()
    ############################################################
    # 역할
    #   컬렉션(list, tuple, set, dict 등)의 데이터를 정렬하여
    #   새로운 리스트(List)를 반환한다.
    #
    # 특징
    #   - 기본 정렬은 오름차순(ascending)이다.
    #   - 원본 데이터는 변경하지 않는다.
    #   - 항상 새로운 리스트를 생성하여 반환한다.
    #   - 문자열은 사전순으로 정렬된다.
    #   - Path 객체는 경로 문자열 기준으로 정렬된다.
    #
    # 주요 파라미터
    #
    # iterable
    #   정렬할 대상 컬렉션
    #
    #   예)
    #   sorted([3, 1, 2])
    #   sorted(("c", "a", "b"))
    #
    # key
    #   정렬 기준을 지정하는 함수
    #
    #   예)
    #   sorted(users, key=lambda x: x.name)
    #
    # reverse
    #   True : 내림차순 정렬
    #   False : 오름차순 정렬(기본값)
    #
    #   예)
    #   sorted(numbers, reverse=True)
    #
    # 반환값(Return)
    #
    #   정렬된 새로운 List 객체 반환
    #
    #   예)
    #   numbers = [3, 1, 2]
    #   result = sorted(numbers)
    #
    #   result
    #   [1, 2, 3]
    #
    # 함수 시그니처
    #
    #   sorted(
    #       iterable,
    #       *,
    #       key=None,
    #       reverse=False
    #   ) -> list
    #
    ############################################################
    







def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    긴 문서를 여러 개의 Chunk로 분할한다.

    RAG에서는 문서 전체를 하나의 Embedding으로 생성하지 않고,
    일정 크기의 Chunk로 분할한 후 Chunk 단위로 Embedding을 생성한다.

    이 함수는 단순 글자 수(Character) 기준으로 문서를 분할하며,
    Chunk 경계에서 문맥(Context)이 끊어지는 것을 방지하기 위해
    overlap 크기만큼 이전 Chunk의 내용을 다음 Chunk에 중복 포함한다.

    처리 순서:
        1. 텍스트 정제(clean_text)
        2. chunk_size 단위로 텍스트 분할
        3. overlap 만큼 이전 내용 중복 포함
        4. Chunk 목록 반환

    예시:

        원본 텍스트:
            ABCDEFGHIJKLMNOP

        chunk_size = 8
        overlap = 2

        결과:
            ABCDEFGH
                  GHIJKLMN
                        MNOP

    파라미터:
        text:
            분할할 원본 문서

        chunk_size:
            Chunk 하나의 최대 크기

        overlap:
            Chunk 간 중복 포함할 크기

    리턴값:
        list[str]
            분할된 Chunk 목록

    참고:
        현재는 단순 문자 수 기준 Chunking을 사용한다.

        실무에서는 다음과 같은 구조 기반 Chunking을 함께 고려한다.

        - 문단 단위 Chunking
        - 제목(Header) 기반 Chunking
        - 페이지 단위 Chunking
        - 슬라이드 단위 Chunking
        - 표(Table) 단위 Chunking
        - Semantic Chunking
    """
    text = clean_text(text)

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size는 1 이상이어야 합니다.")

    if overlap < 0:
        raise ValueError("overlap은 0 이상이어야 합니다.")

    if overlap >= chunk_size:
        raise ValueError("overlap은 chunk_size보다 작아야 합니다.")

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def print_record_summary(title: str, count: int, output_path: Path) -> None:
    """스크립트 실행 결과를 보기 좋게 출력한다."""
    print("=" * 80)
    print(title)
    print("-" * 80)
    print(f"생성 건수: {count}")
    print(f"출력 파일: {output_path}")
    print("=" * 80)
