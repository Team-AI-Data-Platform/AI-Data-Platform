import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "microserver_docs"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def main():
    #query = "MicroServer에서 Maven 멀티모듈 구조는 어떻게 되어 있어?"
    query = "API Gateway는 어떤 역할을 해?"

    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode([query]).tolist()[0]

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )

    print(f"질문: {query}")
    print("=" * 80)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for index, document in enumerate(documents):
        print(f"[검색 결과 {index + 1}]")
        print(f"거리: {distances[index]}")
        print(f"메타데이터: {metadatas[index]}")
        print("문서 내용:")
        print(document)
        print("-" * 80)


if __name__ == "__main__":
    main()