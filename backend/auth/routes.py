from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from backend.auth.models import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse
)

from backend.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

from backend.database.connection import get_db
from backend.database.models import User


# ============================================================
# AUTHENTICATION ROUTER
# ============================================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ============================================================
# REGISTER
# ============================================================

@router.post(
    "/register",
    response_model=TokenResponse
)
def register(
    user: RegisterRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Convert email to lowercase
    # --------------------------------------------------------

    email = user.email.lower()

    # --------------------------------------------------------
    # Check whether user already exists
    # --------------------------------------------------------

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    # --------------------------------------------------------
    # Hash password
    # --------------------------------------------------------

    hashed_password = hash_password(
        user.password
    )

    # --------------------------------------------------------
    # Create new database user
    # --------------------------------------------------------

    new_user = User(
        name=user.name,
        email=email,
        password=hashed_password
    )

    # --------------------------------------------------------
    # Save user to database
    # --------------------------------------------------------

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # --------------------------------------------------------
    # Create JWT access token
    # --------------------------------------------------------

    access_token = create_access_token(
        data={
            "sub": email
        }
    )

    # --------------------------------------------------------
    # Return token
    # --------------------------------------------------------

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Convert email to lowercase
    # --------------------------------------------------------

    email = user.email.lower()

    # --------------------------------------------------------
    # Find user in database
    # --------------------------------------------------------

    stored_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    # --------------------------------------------------------
    # User does not exist
    # --------------------------------------------------------

    if not stored_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # --------------------------------------------------------
    # Verify password
    # --------------------------------------------------------

    if not verify_password(
        user.password,
        stored_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # --------------------------------------------------------
    # Create JWT access token
    # --------------------------------------------------------

    access_token = create_access_token(
        data={
            "sub": email
        }
    )

    # --------------------------------------------------------
    # Return token
    # --------------------------------------------------------

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ============================================================
# CURRENT USER
# ============================================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------------
    # Return authenticated user
    # --------------------------------------------------------

    return current_user