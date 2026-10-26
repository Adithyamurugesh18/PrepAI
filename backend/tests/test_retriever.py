import numpy as np
from unittest.mock import MagicMock

from backend.rag import retriever


def test_retrieve_documents_success(monkeypatch):
    """Test successful document retrieval."""

    # Mock embedding model
    mock_model = MagicMock()

    # SentenceTransformer.encode() returns a NumPy array
    mock_model.encode.return_value = np.array(
        [[0.1, 0.2, 0.3]]
    )

    # Mock ChromaDB collection
    mock_collection = MagicMock()

    expected_result = {
        "ids": [["doc1", "doc2"]],
        "documents": [
            [
                "Java is a programming language",
                "Python is also a programming language"
            ]
        ]
    }

    mock_collection.query.return_value = expected_result

    # Replace real model and collection with mocks
    monkeypatch.setattr(
        retriever,
        "model",
        mock_model
    )

    monkeypatch.setattr(
        retriever,
        "collection",
        mock_collection
    )

    # Run function
    result = retriever.retrieve_documents(
        "What is Java?",
        top_k=2
    )

    # Verify embedding generation
    mock_model.encode.assert_called_once_with(
        ["What is Java?"]
    )

    # Verify ChromaDB query
    mock_collection.query.assert_called_once_with(
        query_embeddings=[[0.1, 0.2, 0.3]],
        n_results=2
    )

    # Verify result
    assert result == expected_result


def test_retrieve_documents_default_top_k(monkeypatch):
    """Test that the default top_k value is 5."""

    # Mock embedding model
    mock_model = MagicMock()

    mock_model.encode.return_value = np.array(
        [[0.5, 0.6, 0.7]]
    )

    # Mock ChromaDB collection
    mock_collection = MagicMock()

    expected_result = {
        "ids": [
            [
                "doc1",
                "doc2",
                "doc3",
                "doc4",
                "doc5"
            ]
        ]
    }

    mock_collection.query.return_value = expected_result

    # Replace real objects with mocks
    monkeypatch.setattr(
        retriever,
        "model",
        mock_model
    )

    monkeypatch.setattr(
        retriever,
        "collection",
        mock_collection
    )

    # Run function without specifying top_k
    result = retriever.retrieve_documents(
        "What is Python?"
    )

    # Verify embedding generation
    mock_model.encode.assert_called_once_with(
        ["What is Python?"]
    )

    # Verify default top_k = 5
    mock_collection.query.assert_called_once_with(
        query_embeddings=[[0.5, 0.6, 0.7]],
        n_results=5
    )

    # Verify result
    assert result == expected_result


def test_retrieve_documents_empty_query(monkeypatch):
    """Test retrieval with an empty query."""

    # Mock embedding model
    mock_model = MagicMock()

    mock_model.encode.return_value = np.array(
        [[0.0, 0.0, 0.0]]
    )

    # Mock ChromaDB collection
    mock_collection = MagicMock()

    expected_result = {
        "ids": [[]],
        "documents": [[]]
    }

    mock_collection.query.return_value = expected_result

    # Replace real objects with mocks
    monkeypatch.setattr(
        retriever,
        "model",
        mock_model
    )

    monkeypatch.setattr(
        retriever,
        "collection",
        mock_collection
    )

    # Run function
    result = retriever.retrieve_documents(
        "",
        top_k=5
    )

    # Verify embedding generation
    mock_model.encode.assert_called_once_with(
        [""]
    )

    # Verify ChromaDB query
    mock_collection.query.assert_called_once_with(
        query_embeddings=[[0.0, 0.0, 0.0]],
        n_results=5
    )

    # Verify result
    assert result == expected_result