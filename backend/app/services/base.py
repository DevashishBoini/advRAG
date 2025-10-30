"""
Base service class for business logic.
"""


class BaseService:
    """Base service class to be inherited by specific services."""

    def __init__(self):
        """Initialize the base service."""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
