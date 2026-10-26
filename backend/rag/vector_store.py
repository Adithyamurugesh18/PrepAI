import chromadb
from embeddings_generator import model
from text_splitter import all_chunks


# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")


# Create or get collection
collection = client.get_or_create_collection(name="prepAI_knowledge")


# Prepare texts
texts = [chunk["text"] for chunk in all_chunks]


# Generate embeddings
embeddings = model.encode(texts).tolist()


# Prepare IDs
ids = [
    f"{chunk['source']}_{chunk['chunk_id']}"
    for chunk in all_chunks
]


# Prepare metadata
metadatas = [
    {
        "source": chunk["source"],
        "chunk_id": chunk["chunk_id"]
    }
    for chunk in all_chunks
]


# Store everything in ChromaDB
collection.upsert(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas
)


print("================================")
print("ChromaDB storage completed!")
print("Total chunks stored:", collection.count())
print("================================")