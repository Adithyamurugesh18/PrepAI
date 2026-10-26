from pydantic import BaseModel, ConfigDict, EmailStr


# ============================================================
# REGISTER REQUEST
# ============================================================

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


# ============================================================
# LOGIN REQUEST
# ============================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ============================================================
# TOKEN RESPONSE
# ============================================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============================================================
# USER RESPONSE
# ============================================================

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(
        from_attributes=True
    )

    # ============================================================
# CHAT HISTORY RESPONSE
# ============================================================

class ChatHistoryResponse(BaseModel):
    id: int
    user_id: int
    question: str
    answer: str

    model_config = ConfigDict(
        from_attributes=True
    )