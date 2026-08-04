import logging
from datetime import timedelta
from sqlalchemy.orm import Session
from database import crud
from database.schemas import UserCreate, UserResponse, LoginRequest, Token
from core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from core.config import settings
from core.exceptions import MediGuruException, AuthenticationError

logger = logging.getLogger("service.auth")

class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserCreate) -> UserResponse:
        """
        Registers a new user, validating uniqueness and hashing password.
        """
        logger.info(f"Initiating user registration for email: {user_in.email}")
        existing_user = crud.get_user_by_email(db, email=user_in.email)
        if existing_user:
            logger.warning(f"User registration failed: Email {user_in.email} is already registered.")
            raise MediGuruException(message="Email already registered.", status_code=400)

        hashed_password = get_password_hash(user_in.password)
        new_user = crud.create_user(db, user=user_in, hashed_password=hashed_password)
        logger.info(f"User registration successful: User ID {new_user.id}, Email {new_user.email}")
        return UserResponse.model_validate(new_user)

    @staticmethod
    def authenticate_user(db: Session, login_req: LoginRequest) -> Token:
        """
        Authenticates user credentials and returns signed JWT access and refresh tokens.
        """
        logger.info(f"Authenticating user login attempt for email: {login_req.email}")
        user = crud.get_user_by_email(db, email=login_req.email)
        if not user:
            logger.warning(f"Login failed: No user account found with email {login_req.email}")
            raise AuthenticationError(message="Incorrect email or password.")

        if not verify_password(login_req.password, user.password_hash):
            logger.warning(f"Login failed: Password mismatch for user ID {user.id} ({login_req.email})")
            raise AuthenticationError(message="Incorrect email or password.")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = create_access_token(subject=user.id, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(subject=user.id, expires_delta=refresh_token_expires)

        logger.info(f"Authentication successful for user ID {user.id}. Issued access & refresh tokens.")
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
