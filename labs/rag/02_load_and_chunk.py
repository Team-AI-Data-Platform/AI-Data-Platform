from pathlib import Path


def load_markdown(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    return path.read_text(encoding="utf-8")


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - overlap

    return chunks


if __name__ == "__main__":
    document_path = "docs/microserver_guide.md"

    text = load_markdown(document_path)
    chunks = chunk_text(text)

    print(f"원본 문서 길이: {len(text)}")
    print(f"생성된 Chunk 수: {len(chunks)}")

    for idx, chunk in enumerate(chunks, start=1):
        print("=" * 50)
        print(f"Chunk {idx}")
        print(chunk)