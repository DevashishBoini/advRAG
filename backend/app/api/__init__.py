"""
API module for handling HTTP requests and responses.

Architecture:
- router.py - Main router that aggregates all routes
- routes/ - API endpoint definitions (thin layer)
- handlers/ - Business logic for endpoints (core logic)

This follows API-first architecture where:
1. Routes define the API contract (OpenAPI spec)
2. Handlers contain the actual business logic
3. Services provide data access and business rules

Note: The main aggregator is in router.py (not routes.py) to avoid 
naming conflict with the routes/ directory.
"""

from app.api.router import router

__all__ = ["router"]
