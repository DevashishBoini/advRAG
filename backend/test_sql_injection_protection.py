"""
Quick test to demonstrate SQL injection protection in Pydantic models.
Run with: python test_sql_injection_protection.py
"""

from app.models.schemas import SessionCreateRequest, SessionUpdateRequest
from pydantic import ValidationError


def test_sql_injection_protection():
    """Test that SQL injection patterns are rejected."""
    
    print("🔒 Testing SQL Injection Protection\n")
    
    # Test cases with SQL injection attempts
    malicious_titles = [
        "My Session'; DROP TABLE chat_sessions;--",
        "Session -- comment",
        "Normal Title; DELETE FROM users",
        "Session UNION SELECT * FROM passwords",
        "Test EXEC sp_executesql",
        "Valid Session",  # This should pass
    ]
    
    for title in malicious_titles:
        try:
            request = SessionCreateRequest(title=title, user_id="test_user", metadata=None)
            print(f"✅ ALLOWED: '{title}'")
        except ValidationError as e:
            print(f"❌ BLOCKED: '{title}'")
            print(f"   Reason: {e.errors()[0]['msg']}\n")
    
    print("\n" + "="*60)
    print("🎯 Summary:")
    print("- SQLAlchemy ORM provides PRIMARY protection (parameterized queries)")
    print("- Pydantic validators provide SECONDARY protection (defense in depth)")
    print("- Both layers work together for production security")
    print("="*60)


if __name__ == "__main__":
    test_sql_injection_protection()
