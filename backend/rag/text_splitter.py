from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_loader import load_all_documents
documents = load_all_documents()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

all_chunks = []

for file_name, text in documents.items():

    print("=" * 60)
    print(f"Processing: {file_name}")
    print("=" * 60)

    chunks = splitter.split_text(text)

    print(f"Total Chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks):

        chunk_data = {
            "source": file_name,
            "chunk_id": index + 1,
            "text": chunk
        }

        all_chunks.append(chunk_data)

print(f"Total Chunks Stored: {len(all_chunks)}")
    