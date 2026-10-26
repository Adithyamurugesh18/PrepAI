from datetime import datetime, timedelta, timezone
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import User


# ============================================================
# JWT CONFIGURATION
# ============================================================

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "change-this-secret-key-in-production"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ============================================================
# PASSWORD HASHING
# ============================================================

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Convert a plain password into a secure hash.
    """

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Check whether the entered password
    matches the stored password hash.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ============================================================
# CREATE JWT TOKEN
# ============================================================

def create_access_token(
    data: dict,
    expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# ============================================================
# VERIFY JWT TOKEN
# ============================================================

def verify_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None


# ============================================================
# HTTP BEARER SECURITY
# ============================================================

security = HTTPBearer()


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get the currently authenticated user.

    Flow:

    Authorization header
            ↓
        JWT token
            ↓
      Verify JWT
            ↓
       Get email
            ↓
    Find user in DB
            ↓
       Return User
    """

    # --------------------------------------------------------
    # Get token from Authorization header
    # --------------------------------------------------------

    token = credentials.credentials

    # --------------------------------------------------------
    # Verify JWT
    # --------------------------------------------------------

    payload = verify_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # --------------------------------------------------------
    # Get user email from JWT
    # --------------------------------------------------------

    email = payload.get("sub")

    if not email:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # --------------------------------------------------------
    # Find user in database
    # --------------------------------------------------------

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    # --------------------------------------------------------
    # User does not exist
    # --------------------------------------------------------

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # --------------------------------------------------------
    # Return database User object
    # --------------------------------------------------------

    return user