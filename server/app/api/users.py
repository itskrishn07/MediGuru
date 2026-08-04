import logging
from fastapi import APIRouter, Depends, status
from database.schemas import UserResponse
from database.models import UserORM
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Returns the profile information of the currently authenticated user."
)
async def read_users_me(current_user: UserORM = Depends(get_current_user)):
    logger.debug(f"Fetching profile for user ID: {current_user.id}")
    return current_user
