from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.api.api import app
from backend.auth.security import get_current_user
from backend.database.connection import get_db


# ------------------------------------------------------------
# Fake authenticated user
# ------------------------------------------------------------

fake_user = SimpleNamespace(
    id=1,
    email="test@example.com"
)


# ------------------------------------------------------------
# Fake database session
# ------------------------------------------------------------

mock_db = MagicMock()


def override_current_user():
    return fake_user


def override_get_db():
    yield mock_db


# Override FastAPI dependencies
app.dependency_overrides[get_current_user] = override_current_user
app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


# ============================================================
# TEST HOME ENDPOINT
# ============================================================

def test_home():
    """
    Test that the home endpoint is working.
    """

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "PrepAI API is running"
    }


# ============================================================
# TEST CHAT ENDPOINT
# ============================================================

def test_chat_success():
    """
    Test the /api/chat endpoint.

    It should:
    1. Accept a question
    2. Call the RAG pipeline
    3. Save chat history
    4. Return question, answer and user email
    """

    mock_db.reset_mock()

    with patch(
        "backend.api.api.ask_question",
        return_value="Python is a programming language."
    ) as mock_ask_question:

        response = client.post(
            "/api/chat",
            json={
                "question": "What is Python?"
            }
        )

    # Check HTTP response
    assert response.status_code == 200

    # Check response data
    data = response.json()

    assert data["question"] == "What is Python?"
    assert data["answer"] == "Python is a programming language."
    assert data["user"] == "test@example.com"

    # Verify RAG pipeline was called
    mock_ask_question.assert_called_once_with(
        "What is Python?"
    )

    # Verify database operations
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()