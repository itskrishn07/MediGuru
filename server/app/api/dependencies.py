import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.database import get_db
from database import crud
from database.models import UserORM
from core.security import decode_token
from core.logger import user_id_ctx

logger = logging.getLogger(__name__)

# Configures OAuth2 Bearer scheme for retrieving JWT from Authorization headers
oauth2_scheme = HTTPBearer()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserORM:
    """
    Dependency to retrieve the currently authenticated user from the JWT access token.
    Populates user_id in logging context.
    Raises HTTP 401 Unauthorized if the token is invalid, expired, or user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token.credentials)
    if payload is None:
        logger.warning("Token decoding failed or token signature invalid.")
        raise credentials_exception
        
    token_type = payload.get("type")
    if token_type != "access":
        logger.warning(f"Expected access token, received: {token_type}")
        raise credentials_exception
        
    user_id_str = payload.get("sub")
    if user_id_str is None:
        logger.warning("Token payload missing 'sub' subject claim.")
        raise credentials_exception
        
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.warning(f"Invalid user ID format in token payload: {user_id_str}")
        raise credentials_exception
        
    user = crud.get_user_by_id(db, user_id=user_id)
    if user is None:
        logger.warning(f"Authenticated user ID {user_id} not found in database.")
        raise credentials_exception

    # Populate user_id in logging context for request correlation
    user_id_ctx.set(str(user.id))
    logger.debug(f"User authenticated successfully: ID {user.id}")
        
    return user
