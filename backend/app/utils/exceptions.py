"""
Custom exception classes for better error handling.
"""


class AppException(Exception):
    """Base exception class for application errors."""
    
    def __init__(self, message: str, detail: str | None = None):
        """
        Initialize exception.
        
        Args:
            message: Short error message
            detail: Optional detailed error information
        """
        self.message = message
        self.detail = detail
        super().__init__(message)
    
    def to_dict(self) -> dict:
        """
        Convert exception to dictionary for API responses.
        
        Returns:
            dict: Exception data
        """
        return {
            "message": self.message,
            "detail": self.detail
        }


class ValidationError(AppException):
    """Raised when input validation fails."""
    pass


class ResourceNotFoundError(AppException):
    """Raised when a requested resource is not found."""
    pass


class DatabaseError(AppException):
    """Raised when database operations fail."""
    pass


class ConnectionError(AppException):
    """Raised when external connection fails."""
    pass


class AuthenticationError(AppException):
    """Raised when authentication fails."""
    pass


class AuthorizationError(AppException):
    """Raised when authorization fails."""
    pass


class RateLimitError(AppException):
    """Raised when rate limit is exceeded."""
    pass
