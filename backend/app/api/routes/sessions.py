"""
Session API routes.
Defines REST endpoints for session management.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.api.handlers.session_handlers import (
    handle_create_session,
    handle_delete_session,
    handle_get_session,
    handle_list_sessions,
    handle_update_session,
)
from app.models.schemas import (
    ErrorResponse,
    SessionCreateRequest,
    SessionResponse,
    SessionUpdateRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Session created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Resource not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
        503: {"model": ErrorResponse, "description": "Service unavailable"},
    },
    summary="Create a new chat session",
    description="Creates a new chat session and returns welcome message",
)
async def create_session(request: SessionCreateRequest) -> SessionResponse:
    """
    Create a new chat session.
    
    - **user_id**: Optional user identifier
    - **title**: Optional session title (defaults to "New Chat Session")
    - **metadata**: Optional metadata dictionary
    
    Returns session with message: "hello! upload docs for me to Index"
    """
    return await handle_create_session(request)


@router.get(
    "/{session_id}",
    response_model=SessionResponse,
    responses={
        200: {"description": "Session retrieved successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Session not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Get a session by ID",
    description="Retrieves a specific chat session by its UUID",
)
async def get_session(session_id: UUID) -> SessionResponse:
    """
    Get a chat session by ID.
    
    - **session_id**: UUID of the session to retrieve
    """
    return await handle_get_session(session_id)


@router.get(
    "",
    response_model=list[SessionResponse],
    responses={
        200: {"description": "Sessions retrieved successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="List sessions",
    description="Lists chat sessions with optional filtering and pagination",
)
async def list_sessions(
    user_id: str | None = Query(None, max_length=255, description="Filter by user ID"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
) -> list[SessionResponse]:
    """
    List chat sessions with optional filtering.
    
    - **user_id**: Optional filter by user ID (validated for security)
    - **limit**: Maximum number of results (1-100, default: 50)
    - **offset**: Pagination offset (default: 0)
    
    Note: user_id is validated in the service layer for security.
    """
    return await handle_list_sessions(user_id, limit, offset)


@router.patch(
    "/{session_id}",
    response_model=SessionResponse,
    responses={
        200: {"description": "Session updated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Session not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Update a session",
    description="Updates a chat session's properties",
)
async def update_session(
    session_id: UUID,
    request: SessionUpdateRequest
) -> SessionResponse:
    """
    Update a chat session.
    
    - **session_id**: UUID of the session to update
    - **title**: Optional new title
    - **status**: Optional new status
    - **is_active**: Optional active status
    - **metadata**: Optional new metadata
    """
    return await handle_update_session(session_id, request)


@router.delete(
    "/{session_id}",
    response_model=SessionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Session deleted successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Session not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Delete a session",
    description="Soft deletes a chat session and returns the deleted resource",
)
async def delete_session(session_id: UUID) -> SessionResponse:
    """
    Delete a chat session (soft delete).
    
    - **session_id**: UUID of the session to delete
    
    Returns the deleted session resource with confirmation message.
    The session is not actually deleted but marked as inactive/archived.
    """
    deleted_session = await handle_delete_session(session_id)
    return deleted_session
