from backend.rag.retriever import retrieve_documents
from backend.rag.llm_service import generate_answer


def ask_question(question):
    """
    Complete RAG pipeline:
    Question → Retriever → Context → Gemini → Answer
    """

    # Retrieve relevant documents
    results = retrieve_documents(question)

    # Get retrieved documents
    documents = results["documents"][0]

    # Combine documents into context
    context = "\n\n".join(documents)

    # Generate answer using Gemini
    answer = generate_answer(question, context)

    return answer