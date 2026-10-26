from pathlib import Path
from pypdf import PdfReader

# Path to raw documents
DATA_FOLDER = Path("data/raw")


def read_pdf(pdf_path: Path) -> str:
    """
    Reads one PDF file and returns all extracted text.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def load_all_documents():

    documents = {}

    # Find every PDF inside data/raw
    pdf_files = DATA_FOLDER.rglob("*.pdf")

    for pdf in pdf_files:

        print(f"\nReading: {pdf.name}")

        text = read_pdf(pdf)

        documents[pdf.name] = text

    return documents


if __name__ == "__main__":

    documents = load_all_documents()

    print("\n")
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"\nTotal Documents : {len(documents)}")

    for file_name, text in documents.items():

        print("\n")
        print("=" * 60)
        print(file_name)
        print("=" * 60)

        print(text[:300])

        print("\nCharacters :", len(text))