from typing import Optional, Dict, Any

class CognitionError(Exception):
    """Base exception for all Cognition SDK errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, trace_id: Optional[str] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.trace_id = trace_id
        self.body = body or {}

class BadRequestError(CognitionError):
    """Exception raised for 400 Bad Request errors."""
    pass

class AuthenticationError(CognitionError):
    """Exception raised for 401 Unauthorized errors."""
    pass

class RateLimitError(CognitionError):
    """Exception raised for 429 Too Many Requests errors."""
    pass

class ServerError(CognitionError):
    """Exception raised for 5xx Server errors."""
    pass

def make_status_error(status_code: int, body: Dict[str, Any]) -> CognitionError:
    """Helper to create the appropriate exception from an HTTP response."""
    message = body.get("details") or body.get("title") or "Unknown error"
    trace_id = body.get("trace_id")
    
    if status_code == 400:
        return BadRequestError(message, status_code, trace_id, body)
    elif status_code == 401:
        return AuthenticationError(message, status_code, trace_id, body)
    elif status_code == 429:
        return RateLimitError(message, status_code, trace_id, body)
    elif status_code >= 500:
        return ServerError(message, status_code, trace_id, body)
    
    return CognitionError(message, status_code, trace_id, body)
