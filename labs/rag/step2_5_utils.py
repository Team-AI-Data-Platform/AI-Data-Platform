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
    입력값을 기반으로 항상 동일한 ID를 생성한다.
    Vector DB에 저장할 문서 ID로 사용한다.
    """
    raw = "|".join(str(part) for part in parts)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> int:
    """
    JSONL 파일을 저장한다.
    한 줄에 하나의 JSON 객체를 기록한다.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0

    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1

    return count


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """JSONL 파일을 읽어서 dict 목록으로 반환한다."""
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

    #(ext.lower() for ext in extensions)를
    # Generator Expression(제너레이터 표현식) 이라고 한다.
    # 파이썬 에서는 [x.lower() for x in extensions] 게 하면 리스트가 만들어지고
    # (x.lower() for x in extensions) 게 쓰면 제너레이터가 만들어 진다.
    #   tuple(...)     tuple() 함수가 값을 하나씩 꺼냄     튜플로 변환
    ### 함수의 유일한 인자로 제너레이터를 넘길 때는 바깥 괄호를 생략할 수 있다.
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
        if path.is_file() and path.suffix.lower() in lower_extensions:
            results.append(path)

    return sorted(results)


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    긴 텍스트를 Chunk 단위로 분리한다.

    단순 글자 수 기준 Chunking이다.
    실무에서는 문단, 제목, 페이지, 슬라이드, 표 구조를 함께 고려하는 것이 좋다.
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
