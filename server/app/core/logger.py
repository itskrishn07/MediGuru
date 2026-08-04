import sys
import logging
import contextvars
from pathlib import Path
from logging.handlers import RotatingFileHandler
from core.config import BASE_DIR, settings

# Context variables for request tracking across async execution calls
request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")
user_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("user_id", default="-")

class ContextFilter(logging.Filter):
    """
    Injects request_id and user_id from contextvars into every LogRecord.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get("-")
        record.user_id = user_id_ctx.get("-")
        return True

def setup_logging() -> None:
    """
    Configures centralized structured logging for the application.
    Sets up console logging and rotating file logging under server/logs/.
    """
    logs_dir = BASE_DIR / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    app_log_file = logs_dir / "app.log"
    error_log_file = logs_dir / "error.log"

    # Context Filter
    context_filter = ContextFilter()

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [req_id=%(request_id)s] [user_id=%(user_id)s] %(name)s: %(message)s"
    )

    # Root Logger Setup
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicates on re-initialization
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    # 1. Console Handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(context_filter)
    root_logger.addHandler(console_handler)

    # 2. General App Rotating File Handler (logs/app.log) - 10MB per file, max 5 backups
    app_file_handler = RotatingFileHandler(
        filename=str(app_log_file),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    app_file_handler.setLevel(logging.INFO)
    app_file_handler.setFormatter(formatter)
    app_file_handler.addFilter(context_filter)
    root_logger.addHandler(app_file_handler)

    # 3. Error Rotating File Handler (logs/error.log) - 10MB per file, max 5 backups
    error_file_handler = RotatingFileHandler(
        filename=str(error_log_file),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    error_file_handler.addFilter(context_filter)
    root_logger.addHandler(error_file_handler)

    # Silence overly verbose third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("pypdf").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)

# Automatically run logging setup on module load
setup_logging()
