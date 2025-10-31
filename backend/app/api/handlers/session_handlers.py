"""
Handler functions for session-related operations.
These functions contain the business logic for session endpoints.
"""

import logging
from uuid import UUID

from app.models.schemas import (
    SessionCreateRequest,
    SessionResponse,
    SessionUpdateRequest,
)
from app.services.session_service import session_service
from app.utils.validators import InputValidator

logger = logging.getLogger(__name__)


async def handle_create_session(request: SessionCreateRequest) -> SessionResponse:
    """
    Handle session creation logic.
    
    Args:
        request: Session creation request
        
    Returns:
        SessionResponse: Created session with welcome message
    """
    logger.info(f"ℹ️  Creating new chat session for user: {request.user_id}")
    
    # Create session using service layer
    new_session = await session_service.create_session(request)
    
    # Prepare response with welcome message
    response_data = new_session.to_dict()
    response_data["message"] = "hello! upload docs for me to Index"
    
    logger.info(f"✅ Successfully created session: {new_session.id}")
    
    return SessionResponse(**response_data)


async def handle_get_session(session_id: UUID) -> SessionResponse:
    """
    Handle session retrieval logic.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        SessionResponse: Session details
    """
    logger.info(f"ℹ️  Fetching session: {session_id}")
    
    chat_session = await session_service.get_session(session_id)
    
    response_data = chat_session.to_dict()
    response_data["message"] = "Session retrieved successfully"
    
    return SessionResponse(**response_data)


async def handle_update_session(
    session_id: UUID, 
    request: SessionUpdateRequest
) -> SessionResponse:
    """
    Handle session update logic.
    
    Args:
        session_id: Unique session identifier
        request: Update request data
        
    Returns:
        SessionResponse: Updated session details
    """
    logger.info(f"ℹ️  Updating session: {session_id}")
    
    updated_session = await session_service.update_session(session_id, request)
    
    response_data = updated_session.to_dict()
    response_data["message"] = "Session updated successfully"
    
    return SessionResponse(**response_data)


async def handle_delete_session(session_id: UUID) -> bool:
    """
    Handle session deletion logic.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        bool: True if deleted successfully
    """
    logger.info(f"ℹ️  Deleting session: {session_id}")
    
    deleted = await session_service.delete_session(session_id)
    
    logger.info(f"✅ Successfully deleted session: {session_id}")
    return True


async def handle_list_sessions(
    user_id: str | None = None,
    limit: int = 50,
    offset: int = 0
) -> list[SessionResponse]:
    """
    Handle session listing logic.
    
    Args:
        user_id: Optional user ID filter (validated for security)
        limit: Maximum number of results
        offset: Pagination offset
        
    Returns:
        List of SessionResponse objects
    """
    # Validate user_id if provided (security check for query param)
    validated_user_id = InputValidator.validate_user_id(user_id, required=False)
    
    logger.info(f"ℹ️  Listing sessions for user: {validated_user_id}, limit: {limit}")
    
    sessions = await session_service.list_sessions(validated_user_id, limit, offset)
    
    # Convert to response models with consistent message
    response_list = []
    for session in sessions:
        session_data = session.to_dict()
        session_data["message"] = "Session retrieved successfully"
        response_list.append(SessionResponse(**session_data))
    
    return response_list
