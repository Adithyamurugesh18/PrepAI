from sentence_transformers import SentenceTransformer

from text_splitter import all_chunks
model = SentenceTransformer("all-MiniLM-L6-v2")
first_chunk = all_chunks[0]
embedding = model.encode(first_chunk["text"])

print(embedding)
model = SentenceTransformer("all-MiniLM-L6-v2")
texts = [chunk["text"] for chunk in all_chunks]

embeddings = model.encode(texts)

print("Total chunks:", len(texts))
print("Total embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))