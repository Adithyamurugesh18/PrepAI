from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.rag.rag_pipeline import ask_question

from backend.auth.routes import router as auth_router
from backend.auth.security import get_current_user

from backend.auth.models import ChatHistoryResponse

from backend.database.connection import engine, get_db
from backend.database.models import Base, ChatHistory


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="PrepAI API",
    description="RAG-based AI Interview Preparation Assistant",
    version="1.0.0"
)


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# AUTHENTICATION ROUTES
# ============================================================

app.include_router(auth_router)


# ============================================================
# CHAT REQUEST MODEL
# ============================================================

class QuestionRequest(BaseModel):
    question: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "PrepAI API is running"
    }


# ============================================================
# CHAT
# ============================================================

@app.post("/api/chat")
def chat(
    request: QuestionRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Get authenticated user's ID
    # --------------------------------------------------------

    user_id = current_user.id

    # --------------------------------------------------------
    # Run RAG pipeline
    # --------------------------------------------------------

    answer = ask_question(
        request.question
    )

    # --------------------------------------------------------
    # Create chat history record
    # --------------------------------------------------------

    chat_history = ChatHistory(
        user_id=user_id,
        question=request.question,
        answer=answer
    )

    # --------------------------------------------------------
    # Save chat to database
    # --------------------------------------------------------

    db.add(chat_history)
    db.commit()
    db.refresh(chat_history)

    # --------------------------------------------------------
    # Return response
    # --------------------------------------------------------

    return {
        "question": request.question,
        "answer": answer,
        "user": current_user.email
    }


# ============================================================
# CHAT HISTORY
# ============================================================

@app.get(
    "/api/chat/history",
    response_model=list[ChatHistoryResponse]
)
def get_chat_history(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Get logged-in user's ID
    # --------------------------------------------------------

    user_id = current_user.id

    # --------------------------------------------------------
    # Get only this user's chat history
    # --------------------------------------------------------

    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.id.desc())
        .all()
    )

    # --------------------------------------------------------
    # Return chat history
    # --------------------------------------------------------

    return chats