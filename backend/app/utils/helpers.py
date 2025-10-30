"""
Helper utility functions.
"""

from typing import Any, Optional


def format_response(data: Any, message: Optional[str] = None) -> dict:
    """
    Format API response consistently.
    
    Args:
        data: The response data
        message: Optional message to include
        
    Returns:
        dict: Formatted response
    """
    return {
        "data": data,
        "message": message,
        "success": True,
    }


def format_error(error: str, code: Optional[str] = None) -> dict:
    """
    Format error response consistently.
    
    Args:
        error: Error message
        code: Optional error code
        
    Returns:
        dict: Formatted error response
    """
    return {
        "error": error,
        "code": code,
        "success": False,
    }
