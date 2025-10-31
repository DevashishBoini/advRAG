"""
Service layer for chat session operations.
"""

import json
import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from app.db.manager import db_manager
from app.models.schemas import SessionCreateRequest, SessionUpdateRequest
from app.models.session import ChatSession
from app.utils.exceptions import DatabaseError, ResourceNotFoundError

logger = logging.getLogger(__name__)


class SessionService:
    """
    Service for managing chat sessions.
    
    Provides business logic for CRUD operations on chat sessions
    with proper error handling and logging.
    """
    
    async def create_session(
        self, 
        request: SessionCreateRequest
    ) -> ChatSession:
        """
        Create a new chat session.
        
        Args:
            request: Session creation request data
            
        Returns:
            ChatSession: Created session object
            
        Raises:
            ValidationError: If input validation fails
            DatabaseError: If database operation fails
        """
        try:
            # Pydantic already validated basic fields, only custom validation needed
            logger.info(f"Creating new session for user: {request.user_id}")
            
            # Prepare metadata
            metadata_str = None
            if request.metadata:
                metadata_str = json.dumps(request.metadata)
            
            # Create new session
            new_session = ChatSession(
                user_id=request.user_id,
                title=request.title or "New Chat Session",
                status="active",
                metadata_=metadata_str,
                is_active=True,
                message_count=0,
            )
            
            # Save to database with retry logic
            async def _create():
                async with db_manager.client.get_session() as session:
                    session.add(new_session)
                    await session.flush()
                    await session.refresh(new_session)
                    return new_session
            
            result = await db_manager.execute_with_retry(_create)
            
            logger.info(f"Successfully created session: {result.id}")
            return result
            
        except SQLAlchemyError as e:
            logger.error(f"Database error creating session: {e}")
            raise DatabaseError(
                message="Failed to create session",
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error creating session: {e}")
            raise
    
    async def get_session(self, session_id: UUID) -> ChatSession:
        """
        Get a chat session by ID.
        
        Args:
            session_id: Session UUID
            
        Returns:
            ChatSession: The session object
            
        Raises:
            ResourceNotFoundError: If session not found
            DatabaseError: If database operation fails
        """
        try:
            # FastAPI/Pydantic already validated UUID format
            logger.info(f"Fetching session: {session_id}")
            
            async def _get():
                async with db_manager.client.get_session() as session:
                    result = await session.execute(
                        select(ChatSession).where(ChatSession.id == session_id)
                    )
                    return result.scalar_one_or_none()
            
            chat_session = await db_manager.execute_with_retry(_get)
            
            if not chat_session:
                logger.warning(f"Session not found: {session_id}")
                raise ResourceNotFoundError(
                    message="Session not found",
                    detail=f"No session found with ID: {session_id}"
                )
            
            logger.info(f"Found session: {session_id}")
            return chat_session
            
        except ResourceNotFoundError:
            # Re-raise as-is
            raise
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching session {session_id}: {e}")
            raise DatabaseError(
                message="Failed to fetch session",
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error fetching session {session_id}: {e}")
            raise
    
    async def update_session(
        self,
        session_id: UUID,
        request: SessionUpdateRequest
    ) -> ChatSession:
        """
        Update a chat session.
        
        Args:
            session_id: Session UUID
            request: Update request data
            
        Returns:
            ChatSession: Updated session object
            
        Raises:
            ResourceNotFoundError: If session not found
            DatabaseError: If database operation fails
        """
        try:
            # FastAPI/Pydantic already validated inputs
            logger.info(f"Updating session: {session_id}")
            
            # Build update data - Pydantic already validated
            update_data = {}
            if request.title is not None:
                update_data["title"] = request.title
            if request.status is not None:
                update_data["status"] = request.status
            if request.is_active is not None:
                update_data["is_active"] = request.is_active
            if request.metadata is not None:
                update_data["metadata_"] = json.dumps(request.metadata)
            
            if not update_data:
                logger.warning("No update data provided")
                return await self.get_session(session_id)
            
            async def _update():
                async with db_manager.client.get_session() as session:
                    await session.execute(
                        update(ChatSession)
                        .where(ChatSession.id == session_id)
                        .values(**update_data)
                    )
                    result = await session.execute(
                        select(ChatSession).where(ChatSession.id == session_id)
                    )
                    return result.scalar_one_or_none()
            
            updated_session = await db_manager.execute_with_retry(_update)
            
            if not updated_session:
                logger.warning(f"Session not found for update: {session_id}")
                raise ResourceNotFoundError(
                    message="Session not found",
                    detail=f"No session found with ID: {session_id}"
                )
            
            logger.info(f"Successfully updated session: {session_id}")
            return updated_session
            
        except ResourceNotFoundError:
            # Re-raise as-is
            raise
        except SQLAlchemyError as e:
            logger.error(f"Database error updating session {session_id}: {e}")
            raise DatabaseError(
                message="Failed to update session",
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error updating session {session_id}: {e}")
            raise
    
    async def list_sessions(
        self,
        user_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> list[ChatSession]:
        """
        List chat sessions with optional filtering.
        
        Args:
            user_id: Optional user ID filter
            limit: Maximum number of results
            offset: Pagination offset
            
        Returns:
            list[ChatSession]: List of session objects
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            # FastAPI/Pydantic already validated inputs (Query params have validation)
            logger.info(f"Listing sessions for user: {user_id}, limit: {limit}")
            
            async def _list():
                async with db_manager.client.get_session() as session:
                    query = select(ChatSession)
                    
                    if user_id:
                        query = query.where(ChatSession.user_id == user_id)
                    
                    query = query.order_by(ChatSession.created_at.desc())
                    query = query.limit(limit).offset(offset)
                    
                    result = await session.execute(query)
                    return result.scalars().all()
            
            sessions = await db_manager.execute_with_retry(_list)
            logger.info(f"Found {len(sessions)} sessions")
            return list(sessions)
            
        except SQLAlchemyError as e:
            logger.error(f"Database error listing sessions: {e}")
            raise DatabaseError(
                message="Failed to list sessions",
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error listing sessions: {e}")
            raise
    
    async def delete_session(self, session_id: UUID) -> ChatSession:
        """
        Delete a chat session (soft delete by marking inactive).
        
        Args:
            session_id: Session UUID
            
        Returns:
            ChatSession: The deleted session object
            
        Raises:
            ResourceNotFoundError: If session not found
            DatabaseError: If database operation fails
        """
        try:
            # FastAPI/Pydantic already validated UUID
            logger.info(f"Deleting session: {session_id}")
            
            async def _delete():
                async with db_manager.client.get_session() as session:
                    # Update session to mark as deleted
                    await session.execute(
                        update(ChatSession)
                        .where(ChatSession.id == session_id)
                        .values(is_active=False, status="archived")
                    )
                    # Fetch and return the updated session
                    result = await session.execute(
                        select(ChatSession).where(ChatSession.id == session_id)
                    )
                    return result.scalar_one_or_none()
            
            deleted_session = await db_manager.execute_with_retry(_delete)
            
            if not deleted_session:
                logger.warning(f"Session not found for deletion: {session_id}")
                raise ResourceNotFoundError(
                    message="Session not found",
                    detail=f"No session found with ID: {session_id}"
                )
            
            logger.info(f"Successfully deleted session: {session_id}")
            return deleted_session
            
        except ResourceNotFoundError:
            # Re-raise as-is
            raise
        except SQLAlchemyError as e:
            logger.error(f"Database error deleting session {session_id}: {e}")
            raise DatabaseError(
                message="Failed to delete session",
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            raise


# Global session service instance
session_service = SessionService()
