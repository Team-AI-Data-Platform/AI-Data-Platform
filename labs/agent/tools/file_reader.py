from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


def read_text_file(relative_path: str) -> str:
    """
    labs/agent 디렉터리 내부의 텍스트 파일을 읽는다.

    Args:
        relative_path:
            labs/agent 디렉터리를 기준으로 한 상대 경로.
            예: "sample_docs/agent_sample.md"

    Returns:
        파일 내용을 문자열로 반환한다.

    Raises:
        ValueError:
            경로가 비어 있거나, labs/agent 밖의 파일을 읽으려는 경우 발생한다.

        FileNotFoundError:
            파일이 존재하지 않는 경우 발생한다.
    """
    if not relative_path or not relative_path.strip():
        raise ValueError("파일 경로가 비어 있습니다.")

    target_path = (BASE_DIR / relative_path).resolve()

    if not str(target_path).startswith(str(BASE_DIR)):
        raise ValueError("labs/agent 디렉터리 밖의 파일은 읽을 수 없습니다.")

    if not target_path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {target_path}")

    if not target_path.is_file():
        raise ValueError(f"파일이 아닙니다: {target_path}")

    return target_path.read_text(encoding="utf-8")
