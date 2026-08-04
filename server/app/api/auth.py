import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db
from database.schemas import UserCreate, UserResponse, LoginRequest, Token
from services.auth_service import AuthService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Registers a new user in the system with validated email and hashed password."
)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(db=db, user_in=user_in)

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticates user credentials and returns signed JWT access and refresh tokens."
)
async def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.authenticate_user(db=db, login_req=login_req)
