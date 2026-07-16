import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db
from database import crud
from database.schemas import UserCreate, UserResponse, LoginRequest, Token
from core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user in the system.
    Validates email format, password strength, and ensures no duplicate registrations.
    """
    # 1. Check if user already exists
    existing_user = crud.get_user_by_email(db, email=user_in.email)
    if existing_user:
        logger.warning(f"Registration attempt failed: Email {user_in.email} already registered.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
        
    # 2. Hash the password securely
    try:
        hashed_password = get_password_hash(user_in.password)
    except Exception as e:
        logger.error(f"Failed to hash password during registration: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing registration."
        )
        
    # 3. Create the user in the database
    new_user = crud.create_user(db, user=user_in, hashed_password=hashed_password)
    logger.info(f"User successfully registered: ID {new_user.id}, Email {new_user.email}")
    return new_user

@router.post("/login", response_model=Token)
async def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a signed JWT access and refresh token.
    """
    # 1. Fetch user by email
    user = crud.get_user_by_email(db, email=login_req.email)
    if not user:
        logger.warning(f"Login attempt failed: Email {login_req.email} not found.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 2. Verify password
    if not verify_password(login_req.password, user.password_hash):
        logger.warning(f"Login attempt failed: Incorrect password for email {login_req.email}.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Generate tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(subject=user.id, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(subject=user.id, expires_delta=refresh_token_expires)
    
    logger.info(f"User successfully logged in: ID {user.id}")
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
