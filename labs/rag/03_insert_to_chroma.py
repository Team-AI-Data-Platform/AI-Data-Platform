from pathlib import Path
from uuid import uuid4

import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "microserver_docs"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


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


def main():
    document_path = "docs/microserver_guide.md"

    text = load_markdown(document_path)
    chunks = chunk_text(text)

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(chunks).tolist()

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    ids = [str(uuid4()) for _ in chunks]

    metadatas = [
        {
            "source": document_path,
            "chunk_index": index,
            "document_type": "markdown",
            "project": "MicroServer"
        }
        for index, _ in enumerate(chunks)
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"문서 적재 완료")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"적재 Chunk 수: {len(chunks)}")


if __name__ == "__main__":
    main()