"""
Input validation utilities.
Provides reusable validators for common input fields.
"""

import json
import re
from typing import Any
from uuid import UUID

from app.utils.exceptions import ValidationError


class InputValidator:
    """Validator class with reusable validation methods."""
    
    # Constants for validation
    MIN_TITLE_LENGTH = 1
    MAX_TITLE_LENGTH = 500
    MAX_USER_ID_LENGTH = 255
    MAX_METADATA_SIZE = 10000  # 10KB
    MAX_METADATA_KEY_LENGTH = 100
    ALLOWED_STATUS_VALUES = ["active", "completed", "archived", "paused"]
    
    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\bDROP\b|\bDELETE\b|\bINSERT\b|\bUPDATE\b|\bSELECT\b).*\bFROM\b",
        r"--",
        r";.*(\bDROP\b|\bDELETE\b)",
        r"\bEXEC\b|\bEXECUTE\b",
        r"\bUNION\b.*\bSELECT\b",
    ]
    
    @staticmethod
    def validate_title(title: str | None, field_name: str = "title") -> str:
        """
        Validate session title with comprehensive checks.
        
        Validates:
        - Length (min: 1, max: 500 chars)
        - Printable characters only (prevents control characters)
        - SQL injection patterns (defense in depth)
        - Strips whitespace
        
        Args:
            title: Title to validate
            field_name: Name of the field for error messages
            
        Returns:
            str: Validated and sanitized title
            
        Raises:
            ValidationError: If validation fails
        """
        if title is None or title == "":
            return "New Chat Session"  # Default value
        
        # Strip whitespace
        title = title.strip()
        
        # Check minimum length
        if len(title) < InputValidator.MIN_TITLE_LENGTH:
            raise ValidationError(
                message=f"{field_name} is too short",
                detail=f"{field_name} must be at least {InputValidator.MIN_TITLE_LENGTH} character"
            )
        
        # Check maximum length (also validated by Pydantic Field, but keep for direct usage)
        if len(title) > InputValidator.MAX_TITLE_LENGTH:
            raise ValidationError(
                message=f"{field_name} is too long",
                detail=f"{field_name} must not exceed {InputValidator.MAX_TITLE_LENGTH} characters"
            )
        
        # Check for invalid characters (only allow printable characters)
        if not title.isprintable():
            raise ValidationError(
                message=f"{field_name} contains invalid characters",
                detail="Only printable characters are allowed"
            )
        
        # Check for SQL injection patterns (defense in depth)
        for pattern in InputValidator.SQL_INJECTION_PATTERNS:
            if re.search(pattern, title, re.IGNORECASE):
                raise ValidationError(
                    message=f"{field_name} contains potentially unsafe content",
                    detail="Please use a different title"
                )
        
        return title
    
    @staticmethod
    def validate_uuid(value: str | UUID, field_name: str = "id") -> UUID:
        """
        Validate UUID format.
        
        Args:
            value: UUID string or UUID object
            field_name: Name of the field for error messages
            
        Returns:
            UUID: Validated UUID object
            
        Raises:
            ValidationError: If validation fails
        """
        if isinstance(value, UUID):
            return value
        
        try:
            return UUID(str(value))
        except (ValueError, AttributeError, TypeError) as e:
            raise ValidationError(
                message=f"Invalid {field_name} format",
                detail=f"{field_name} must be a valid UUID"
            )
    
    @staticmethod
    def validate_user_id(user_id: str | None, required: bool = False) -> str | None:
        """
        Validate user ID with security checks.
        
        Validates:
        - Length (max: 255 chars)
        - Valid characters only (alphanumeric, dash, underscore, @, dot)
        - Strips whitespace
        
        Args:
            user_id: User ID to validate
            required: Whether the field is required
            
        Returns:
            str | None: Validated user ID
            
        Raises:
            ValidationError: If validation fails
        """
        if user_id is None:
            if required:
                raise ValidationError(
                    message="user_id is required",
                    detail="User ID must be provided"
                )
            return None
        
        # Strip whitespace
        user_id = user_id.strip()
        
        # Check if empty after stripping
        if not user_id:
            if required:
                raise ValidationError(
                    message="user_id cannot be empty",
                    detail="User ID must not be blank"
                )
            return None
        
        # Check length
        if len(user_id) > InputValidator.MAX_USER_ID_LENGTH:
            raise ValidationError(
                message="user_id is too long",
                detail=f"User ID must not exceed {InputValidator.MAX_USER_ID_LENGTH} characters"
            )
        
        # Check for valid characters (security - prevent injection)
        if not re.match(r'^[a-zA-Z0-9_\-@.]+$', user_id):
            raise ValidationError(
                message="user_id contains invalid characters",
                detail="User ID can only contain letters, numbers, dash, underscore, @ and dot"
            )
        
        return user_id
    
    @staticmethod
    def validate_status(status: str | None) -> str | None:
        """
        Validate session status.
        
        Args:
            status: Status to validate
            
        Returns:
            str | None: Validated status
            
        Raises:
            ValidationError: If validation fails
        """
        if status is None:
            return None
        
        status = status.strip().lower()
        
        if status not in InputValidator.ALLOWED_STATUS_VALUES:
            raise ValidationError(
                message="Invalid status value",
                detail=f"Status must be one of: {', '.join(InputValidator.ALLOWED_STATUS_VALUES)}"
            )
        
        return status
    
    @staticmethod
    def validate_metadata(metadata: dict | None) -> dict | None:
        """
        Validate metadata dictionary with comprehensive checks.
        
        Validates:
        - Total size limit (10KB - DoS prevention)
        - Key types (strings only)
        - Key length limits (100 chars)
        - Value types (prevent arbitrary object serialization)
        
        Args:
            metadata: Metadata to validate
            
        Returns:
            dict | None: Validated metadata
            
        Raises:
            ValidationError: If validation fails
        """
        if metadata is None:
            return None
        
        if not isinstance(metadata, dict):
            raise ValidationError(
                message="Invalid metadata format",
                detail="Metadata must be a dictionary"
            )
        
        # Check size (prevent DoS via extremely large payloads)
        metadata_str = json.dumps(metadata)
        
        if len(metadata_str) > InputValidator.MAX_METADATA_SIZE:
            raise ValidationError(
                message="Metadata is too large",
                detail=f"Metadata must not exceed {InputValidator.MAX_METADATA_SIZE} bytes (10KB)"
            )
        
        # Validate keys and values
        for key, value in metadata.items():
            # Key must be string
            if not isinstance(key, str):
                raise ValidationError(
                    message="Invalid metadata key",
                    detail="All metadata keys must be strings"
                )
            
            # Key length limit
            if len(key) > InputValidator.MAX_METADATA_KEY_LENGTH:
                raise ValidationError(
                    message="Metadata key is too long",
                    detail=f"Metadata key '{key}' exceeds {InputValidator.MAX_METADATA_KEY_LENGTH} characters"
                )
            
            # Check for allowed value types (security - prevent arbitrary object serialization)
            if not isinstance(value, (str, int, float, bool, type(None), list, dict)):
                raise ValidationError(
                    message="Invalid metadata value type",
                    detail=f"Metadata value for key '{key}' has unsupported type. "
                           f"Allowed: str, int, float, bool, None, list, dict"
                )
        
        return metadata
    
    @staticmethod
    def validate_pagination(limit: int, offset: int) -> tuple[int, int]:
        """
        Validate pagination parameters.
        
        Args:
            limit: Maximum number of results
            offset: Pagination offset
            
        Returns:
            tuple[int, int]: Validated (limit, offset)
            
        Raises:
            ValidationError: If validation fails
        """
        if limit < 1:
            raise ValidationError(
                message="Invalid limit value",
                detail="Limit must be at least 1"
            )
        
        if limit > 100:
            raise ValidationError(
                message="Limit too large",
                detail="Limit must not exceed 100"
            )
        
        if offset < 0:
            raise ValidationError(
                message="Invalid offset value",
                detail="Offset must be non-negative"
            )
        
        return limit, offset
    
    @staticmethod
    def sanitize_string(value: str | None) -> str | None:
        """
        Sanitize string input by removing potentially harmful content.
        
        Args:
            value: String to sanitize
            
        Returns:
            str | None: Sanitized string
        """
        if value is None:
            return None
        
        # Strip whitespace
        value = value.strip()
        
        if not value:
            return None
        
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # Remove control characters except newlines and tabs
        value = ''.join(char for char in value if char.isprintable() or char in '\n\t')
        
        return value


# Convenience function for quick validation
def validate_session_input(
    title: str | None = None,
    user_id: str | None = None,
    status: str | None = None,
    metadata: dict | None = None
) -> dict[str, Any]:
    """
    Validate all session input fields at once.
    
    Args:
        title: Session title
        user_id: User identifier
        status: Session status
        metadata: Additional metadata
        
    Returns:
        dict: Dictionary with validated fields
        
    Raises:
        ValidationError: If any validation fails
    """
    validator = InputValidator()
    
    return {
        "title": validator.validate_title(title) if title is not None else "New Chat Session",
        "user_id": validator.validate_user_id(user_id),
        "status": validator.validate_status(status) if status is not None else "active",
        "metadata": validator.validate_metadata(metadata),
    }
