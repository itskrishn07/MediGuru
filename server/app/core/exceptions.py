import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

class MediGuruException(Exception):
    """Base exception for MediGuru application."""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class ResourceNotFoundError(MediGuruException):
    def __init__(self, message: str = "Requested resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class AuthenticationError(MediGuruException):
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

class PermissionDeniedError(MediGuruException):
    def __init__(self, message: str = "Access denied"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)

class DocumentProcessingError(MediGuruException):
    def __init__(self, message: str = "Failed to process medical document"):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(MediGuruException)
    async def mediguru_exception_handler(request: Request, exc: MediGuruException):
        logger.warning(f"Domain Exception: path={request.url.path} status={exc.status_code} detail={exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled Server Error at path={request.url.path}: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error."}
        )
