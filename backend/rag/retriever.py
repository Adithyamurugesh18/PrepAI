import chromadb
from sentence_transformers import SentenceTransformer


# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(name="prepAI_knowledge")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_documents(query, top_k=5):

    # Convert question into embedding
    query_embedding = model.encode([query]).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results


# Test retrieval when this file is run directly
if __name__ == "__main__":

    query = input("Enter your question: ")

    results = retrieve_documents(query)

    print("\n==============================")
    print("RETRIEVED DOCUMENTS")
    print("==============================")

    for i, document in enumerate(results["documents"][0]):

        print(f"\n--- Result {i + 1} ---")
        print(document)