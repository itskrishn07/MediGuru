import uuid
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.logger import request_id_ctx, user_id_ctx

logger = logging.getLogger("api.access")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that:
    1. Generates or extracts a unique X-Request-ID for every request.
    2. Stores request_id in contextvars for log correlation across services.
    3. Logs incoming request details (method, path, client IP, timestamp).
    4. Measures execution duration and logs outgoing response status and latency.
    5. Appends X-Request-ID to response headers.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        # Generate or reuse X-Request-ID from incoming request headers
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        req_token = request_id_ctx.set(request_id)
        usr_token = user_id_ctx.set("-")

        # Retrieve client IP
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        logger.info(f"Incoming Request: {method} {path} | Client IP: {client_ip}")

        try:
            response = await call_next(request)
            process_time = (time.perf_counter() - start_time) * 1000
            status_code = response.status_code

            logger.info(f"Outgoing Response: {method} {path} | Status: {status_code} | Duration: {process_time:.2f}ms")
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as exc:
            process_time = (time.perf_counter() - start_time) * 1000
            logger.error(f"Unhandled Request Exception: {method} {path} | Duration: {process_time:.2f}ms | Error: {str(exc)}", exc_info=True)
            raise exc
        finally:
            # Clean up contextvars tokens
            request_id_ctx.reset(req_token)
            user_id_ctx.reset(usr_token)
