import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.database import get_db
from database import crud
from database.models import UserORM
from core.security import decode_token

logger = logging.getLogger(__name__)

# Configures OAuth2 scheme for retrieving JWT from Authorization headers
oauth2_scheme = HTTPBearer()

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserORM:
    """
    Dependency to retrieve the currently authenticated user from the JWT token.
    Raises 401 Unauthorized if the token is invalid, expired, or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 1. Decode token
    payload = decode_token(token.credentials)
    if payload is None:
        raise credentials_exception
        
    # 2. Verify token type is 'access'
    token_type = payload.get("type")
    if token_type != "access":
        logger.warning(f"Expected access token, but received: {token_type}")
        raise credentials_exception
        
    # 3. Retrieve user ID
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
        
    try:
        user_id = int(user_id_str)
    except ValueError:
        logger.warning(f"Invalid user ID format in token: {user_id_str}")
        raise credentials_exception
        
    # 4. Fetch user from database
    user = crud.get_user_by_id(db, user_id=user_id)
    if user is None:
        logger.warning(f"User with ID {user_id} not found in database")
        raise credentials_exception
        
    return user
