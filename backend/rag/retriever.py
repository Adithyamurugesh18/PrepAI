
import chromadb
from sentence_transformers import SentenceTransformer

# Resources are initialized only when retrieval is requested.
client = None
collection = None
model = None


def _load_resources():
    global client, collection, model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    if collection is None:
        client = chromadb.PersistentClient(path="chroma_db")
        collection = client.get_collection(name="prepAI_knowledge")


def retrieve_documents(query, top_k=5):
    _load_resources()

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results


if __name__ == "__main__":
    query = input("Enter your question: ")
    results = retrieve_documents(query)

    print("\n==============================")
    print("RETRIEVED DOCUMENTS")
    print("==============================")

    for i, document in enumerate(results["documents"][0]):
        print(f"\n--- Result {i + 1} ---")
        print(document)
