"""
Tests for input validation utilities.
"""

import pytest
from uuid import uuid4

from app.utils.validators import InputValidator, validate_session_input
from app.utils.exceptions import ValidationError


class TestTitleValidation:
    """Test title validation."""
    
    def test_valid_title(self):
        """Test valid title."""
        validator = InputValidator()
        result = validator.validate_title("My Chat Session")
        assert result == "My Chat Session"
    
    def test_none_title_returns_default(self):
        """Test None title returns default."""
        validator = InputValidator()
        result = validator.validate_title(None)
        assert result == "New Chat Session"
    
    def test_empty_title_returns_default(self):
        """Test empty title returns default."""
        validator = InputValidator()
        result = validator.validate_title("")
        assert result == "New Chat Session"
    
    def test_whitespace_stripped(self):
        """Test whitespace is stripped."""
        validator = InputValidator()
        result = validator.validate_title("  Spaces  ")
        assert result == "Spaces"
    
    def test_title_too_long(self):
        """Test title too long raises error."""
        validator = InputValidator()
        long_title = "A" * 501
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_title(long_title)
        
        assert "too long" in exc_info.value.message.lower()
    
    def test_sql_injection_pattern(self):
        """Test SQL injection pattern detection."""
        validator = InputValidator()
        malicious = "'; DROP TABLE users; --"
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_title(malicious)
        
        assert "unsafe" in exc_info.value.message.lower()


class TestUUIDValidation:
    """Test UUID validation."""
    
    def test_valid_uuid_string(self):
        """Test valid UUID string."""
        validator = InputValidator()
        uuid_str = str(uuid4())
        result = validator.validate_uuid(uuid_str)
        
        assert str(result) == uuid_str
    
    def test_valid_uuid_object(self):
        """Test valid UUID object."""
        validator = InputValidator()
        uuid_obj = uuid4()
        result = validator.validate_uuid(uuid_obj)
        
        assert result == uuid_obj
    
    def test_invalid_uuid(self):
        """Test invalid UUID raises error."""
        validator = InputValidator()
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_uuid("not-a-uuid")
        
        assert "invalid" in exc_info.value.message.lower()


class TestUserIDValidation:
    """Test user ID validation."""
    
    def test_valid_user_id(self):
        """Test valid user ID."""
        validator = InputValidator()
        result = validator.validate_user_id("user123")
        assert result == "user123"
    
    def test_user_id_with_allowed_chars(self):
        """Test user ID with allowed special characters."""
        validator = InputValidator()
        result = validator.validate_user_id("user_123-test@example.com")
        assert result == "user_123-test@example.com"
    
    def test_none_user_id_not_required(self):
        """Test None user ID when not required."""
        validator = InputValidator()
        result = validator.validate_user_id(None, required=False)
        assert result is None
    
    def test_none_user_id_required(self):
        """Test None user ID when required raises error."""
        validator = InputValidator()
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_user_id(None, required=True)
        
        assert "required" in exc_info.value.message.lower()
    
    def test_user_id_too_long(self):
        """Test user ID too long raises error."""
        validator = InputValidator()
        long_id = "a" * 256
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_user_id(long_id)
        
        assert "too long" in exc_info.value.message.lower()
    
    def test_user_id_invalid_chars(self):
        """Test user ID with invalid characters."""
        validator = InputValidator()
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_user_id("user#$%^&*()")
        
        assert "invalid characters" in exc_info.value.message.lower()


class TestStatusValidation:
    """Test status validation."""
    
    def test_valid_status(self):
        """Test valid status values."""
        validator = InputValidator()
        
        for status in ["active", "completed", "archived", "paused"]:
            result = validator.validate_status(status)
            assert result == status
    
    def test_status_case_insensitive(self):
        """Test status is case-insensitive."""
        validator = InputValidator()
        result = validator.validate_status("ACTIVE")
        assert result == "active"
    
    def test_none_status(self):
        """Test None status."""
        validator = InputValidator()
        result = validator.validate_status(None)
        assert result is None
    
    def test_invalid_status(self):
        """Test invalid status raises error."""
        validator = InputValidator()
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_status("invalid_status")
        
        assert "invalid status" in exc_info.value.message.lower()


class TestMetadataValidation:
    """Test metadata validation."""
    
    def test_valid_metadata(self):
        """Test valid metadata."""
        validator = InputValidator()
        metadata = {"key": "value", "count": 123, "active": True}
        result = validator.validate_metadata(metadata)
        
        assert result == metadata
    
    def test_none_metadata(self):
        """Test None metadata."""
        validator = InputValidator()
        result = validator.validate_metadata(None)
        assert result is None
    
    def test_metadata_not_dict(self):
        """Test non-dict metadata raises error."""
        validator = InputValidator()
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_metadata("not a dict")  # type: ignore
        
        assert "must be a dictionary" in exc_info.value.message.lower()
    
    def test_metadata_too_large(self):
        """Test metadata too large raises error."""
        validator = InputValidator()
        large_metadata = {"key" + str(i): "x" * 1000 for i in range(20)}
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_metadata(large_metadata)
        
        assert "too large" in exc_info.value.message.lower()
    
    def test_metadata_invalid_key(self):
        """Test metadata with non-string key raises error."""
        validator = InputValidator()
        metadata = {123: "value"}
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_metadata(metadata)
        
        assert "key" in exc_info.value.message.lower()


class TestPaginationValidation:
    """Test pagination validation."""
    
    def test_valid_pagination(self):
        """Test valid pagination parameters."""
        validator = InputValidator()
        limit, offset = validator.validate_pagination(50, 0)
        
        assert limit == 50
        assert offset == 0
    
    def test_limit_too_small(self):
        """Test limit too small raises error."""
        validator = InputValidator()
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_pagination(0, 0)
        
        assert "limit" in exc_info.value.message.lower()
    
    def test_limit_too_large(self):
        """Test limit too large raises error."""
        validator = InputValidator()
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_pagination(101, 0)
        
        assert "limit" in exc_info.value.message.lower()
    
    def test_negative_offset(self):
        """Test negative offset raises error."""
        validator = InputValidator()
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_pagination(50, -1)
        
        assert "offset" in exc_info.value.message.lower()


class TestConvenienceFunction:
    """Test validate_session_input convenience function."""
    
    def test_validate_all_fields(self):
        """Test validating all fields at once."""
        result = validate_session_input(
            title="My Session",
            user_id="user123",
            status="active",
            metadata={"key": "value"}
        )
        
        assert result["title"] == "My Session"
        assert result["user_id"] == "user123"
        assert result["status"] == "active"
        assert result["metadata"] == {"key": "value"}
    
    def test_validate_with_defaults(self):
        """Test validation with default values."""
        result = validate_session_input()
        
        assert result["title"] == "New Chat Session"
        assert result["user_id"] is None
        assert result["status"] == "active"
        assert result["metadata"] is None
