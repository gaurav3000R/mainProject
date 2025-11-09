"""FastAPI middleware for logging, error handling, rate limiting."""
from time import time
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.exceptions import AgenticAIException, RateLimitException
from src.utils.logger import app_logger
from src.utils.helpers import generate_request_id


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = generate_request_id()
        request.state.request_id = request_id
        
        start_time = time()
        
        # Log request
        app_logger.info(
            f"Request: {request.method} {request.url.path} | "
            f"Request ID: {request_id} | "
            f"Client: {request.client.host}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time() - start_time
        
        # Log response
        app_logger.info(
            f"Response: {response.status_code} | "
            f"Request ID: {request_id} | "
            f"Duration: {process_time:.3f}s"
        )
        
        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for handling exceptions."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except AgenticAIException as e:
            app_logger.error(f"Custom exception: {e.message} | Status: {e.status_code}")
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": e.message,
                    "status_code": e.status_code
                }
            )
        except Exception as e:
            app_logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "detail": str(e) if app_logger.level == "DEBUG" else None,
                    "status_code": 500
                }
            )


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""
    
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # {ip: [(timestamp, count)]}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host
        current_time = time()
        
        # Clean old entries
        if client_ip in self.requests:
            self.requests[client_ip] = [
                (ts, count) for ts, count in self.requests[client_ip]
                if current_time - ts < self.window_seconds
            ]
        
        # Count requests in current window
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        request_count = sum(count for _, count in self.requests[client_ip])
        
        if request_count >= self.max_requests:
            app_logger.warning(f"Rate limit exceeded for {client_ip}")
            raise RateLimitException(
                f"Rate limit exceeded. Maximum {self.max_requests} requests per {self.window_seconds} seconds."
            )
        
        # Add current request
        self.requests[client_ip].append((current_time, 1))
        
        return await call_next(request)


class CORSHeadersMiddleware(BaseHTTPMiddleware):
    """Add CORS headers to responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        return response
