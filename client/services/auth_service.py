import logging
from typing import Tuple, Dict, Any, Optional
from services.api import APIService

logger = logging.getLogger(__name__)

class AuthService:
    """
    Handles authentication requests to the FastAPI backend endpoints:
    - POST /auth/login
    - POST /auth/register
    - GET /users/me
    """

    @staticmethod
    def login(email: str, password: str) -> Tuple[bool, Any]:
        """
        Authenticates a user and retrieves JWT access & refresh tokens.
        """
        payload = {"email": email, "password": password}
        success, response = APIService.post("auth/login", payload)
        if success:
            logger.info(f"User {email} successfully authenticated via backend.")
            return True, response
        return False, response

    @staticmethod
    def register(full_name: str, email: str, password: str) -> Tuple[bool, Any]:
        """
        Registers a new user in PostgreSQL database.
        """
        payload = {
            "full_name": full_name,
            "email": email,
            "password": password
        }
        success, response = APIService.post("auth/register", payload)
        if success:
            logger.info(f"User {email} registered successfully.")
            return True, response
        return False, response

    @staticmethod
    def get_current_user() -> Tuple[bool, Any]:
        """
        Fetches the authenticated user profile details from backend /users/me.
        """
        success, response = APIService.get("users/me")
        if success:
            return True, response
        return False, response
