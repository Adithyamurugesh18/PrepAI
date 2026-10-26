from unittest.mock import patch

from backend.rag.rag_pipeline import ask_question


def test_ask_question_success():
    """
    Test the complete RAG pipeline:
    Question → Retriever → Context → LLM → Answer
    """

    mock_results = {
        "documents": [
            [
                "Python is a programming language.",
                "Python is commonly used for AI and data science."
            ]
        ]
    }

    with patch(
        "backend.rag.rag_pipeline.retrieve_documents",
        return_value=mock_results
    ) as mock_retrieve, patch(
        "backend.rag.rag_pipeline.generate_answer",
        return_value="Python is a programming language."
    ) as mock_generate:

        result = ask_question("What is Python?")

    # Verify retriever was called correctly
    mock_retrieve.assert_called_once_with("What is Python?")

    # Verify LLM was called with question and combined context
    mock_generate.assert_called_once_with(
        "What is Python?",
        "Python is a programming language.\n\n"
        "Python is commonly used for AI and data science."
    )

    # Verify final answer
    assert result == "Python is a programming language."


def test_ask_question_with_single_document():
    """
    Test RAG pipeline with a single retrieved document.
    """

    mock_results = {
        "documents": [
            ["Java is a programming language."]
        ]
    }

    with patch(
        "backend.rag.rag_pipeline.retrieve_documents",
        return_value=mock_results
    ), patch(
        "backend.rag.rag_pipeline.generate_answer",
        return_value="Java is a programming language."
    ) as mock_generate:

        result = ask_question("What is Java?")

    mock_generate.assert_called_once_with(
        "What is Java?",
        "Java is a programming language."
    )

    assert result == "Java is a programming language."