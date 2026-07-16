import logging
from fastapi import APIRouter, Depends
from database.schemas import UserResponse
from database.models import UserORM
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserORM = Depends(get_current_user)):
    """
    Returns the profile information of the currently authenticated user.
    """
    logger.debug(f"Fetching profile for user ID: {current_user.id}")
    return current_user
