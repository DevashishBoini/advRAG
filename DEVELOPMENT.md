# Development Guide

## Architecture Overview

### System Design
```
Client → FastAPI → Handlers → Services → Database → Supabase PostgreSQL
         ↓
    Middleware (Logging, CORS, Exception Handling)
```

**Layers:**
- **API Layer** (`app/api/`) - Routes, request/response handling
- **Handler Layer** (`app/api/handlers/`) - Endpoint logic, calls services
- **Service Layer** (`app/services/`) - Business logic, validation
- **Database Layer** (`app/db/`) - Connection management, queries
- **Models** (`app/models/`) - SQLAlchemy ORM, Pydantic schemas
- **Utils** (`app/utils/`) - Validation, exceptions, helpers

### Key Components

**Database Management:**
- Connection pooling (default: 20 connections)
- Automatic retry with exponential backoff (max 3 retries)
- Health monitoring
- Async operations with SQLAlchemy 2.0

**Exception Handling:**
- Global exception handlers in `app/api/exception_handlers.py`
- Custom exceptions: `ValidationError`, `ResourceNotFoundError`, `DatabaseError`, `ConnectionError`
- Consistent error responses with proper HTTP status codes

**Validation:**
- Pydantic for basic type/constraint validation
- Custom validators in `app/utils/validators.py` for security (SQL injection, character validation, metadata structure)
- Multi-layer protection: Pydantic → Custom Validators → SQLAlchemy parameterization

**Logging:**
- Request/response middleware
- Structured logging with context
- Configurable log levels

## Setup Instructions

### Prerequisites
- Python 3.11+
- Supabase account
- OpenAI API key

### Quick Setup
```bash
# 1. Install dependencies
pip install -e .

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials:
# - SUPABASE_URL
# - SUPABASE_KEY  
# - DATABASE_URL
# - OPENAI_API_KEY

# 3. Initialize database
python backend/scripts/init_db.py

# 4. Run application
cd backend && python -m app.main
```

### Environment Variables
**Required:**
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key

**Optional (with defaults):**
- `DATABASE_POOL_SIZE=20` - Connection pool size
- `DB_MAX_RETRIES=3` - Max connection retries
- `LOG_LEVEL=INFO` - Logging level
- `ENVIRONMENT=development` - Environment (development/production)

## Implementation Details

### Database Schema

**chat_sessions table:**
```sql
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(500),
    status VARCHAR(50) DEFAULT 'active',
    is_active BOOLEAN DEFAULT true,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_status ON chat_sessions(status);
```

### Validation Rules

**Input Validation:**
- `user_id`: Max 255 chars, alphanumeric + `_-.@`, SQL injection checks
- `title`: 1-500 chars, printable characters only, SQL injection checks
- `status`: Whitelist - ["active", "completed", "archived", "paused"]
- `metadata`: Max 10KB, keys max 100 chars, supports string/number/boolean/null values
- `limit`: 1-100 for pagination
- `offset`: ≥0 for pagination

**Security Features:**
- SQL injection pattern detection (UNION, DROP, SELECT, etc.)
- Character validation (printable, allowed sets)
- Size limits on all inputs
- Metadata structure validation

### Error Handling

**Exception Types:**
- `400` - ValidationError (invalid input)
- `404` - ResourceNotFoundError (session not found)
- `500` - DatabaseError (database operation failed)
- `503` - ConnectionError (database unavailable)

**Response Format:**
```json
{
  "error": "Validation failed",
  "detail": "Title must be between 1 and 500 characters",
  "timestamp": "2025-11-01T12:00:00Z"
}
```

### Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app tests/

# Specific test file
pytest backend/tests/test_sessions.py

# Verbose output
pytest -v
```

**Test Coverage:**
- Session CRUD operations
- Validation logic
- Error handling
- Database retry mechanism

## Code Quality Standards

### Production-Grade Practices
✅ Type hints throughout codebase
✅ Async/await for I/O operations
✅ Connection pooling and retry logic
✅ Comprehensive error handling
✅ Input validation and sanitization
✅ Structured logging
✅ No redundant try-catch blocks (global handlers)
✅ DRY principle (centralized validation)
✅ Proper dependency injection

### Code Organization
- Services use global `db_manager` (no instance storage)
- Handlers delegate to services (no business logic)
- Validation centralized in `InputValidator` class
- Pydantic schemas delegate to custom validators
- No duplicate exception handling

### Configuration Management
- Single source of truth (`app/config.py`)
- Environment-based configuration
- Validation at startup
- Centralized version management

## Development Workflow

### Adding New Features
1. Define database models in `app/models/`
2. Create Pydantic schemas in `app/models/schemas.py`
3. Add validation in `app/utils/validators.py`
4. Implement service logic in `app/services/`
5. Create handlers in `app/api/handlers/`
6. Add routes in `app/api/routes/`
7. Write tests in `backend/tests/`

### Database Changes
1. Update SQLAlchemy models
2. Create migration script
3. Test locally
4. Update documentation

### Debugging
- Check logs for detailed error messages
- Use `/api/v1/health` endpoint for health checks
- Verify database connectivity
- Check environment variables

## Roadmap

**Phase 1: Foundation ✅ COMPLETE**
- Chat session management
- Database setup
- API endpoints
- Error handling

**Phase 2: Document Ingestion 🔜 NEXT**
- File upload API
- Document parsing (PDF, DOCX, TXT, MD)
- Text chunking
- Embedding generation
- Vector storage

**Phase 3: RAG Pipeline 🔜**
- Vector search
- Context retrieval
- LLM integration
- Streaming responses

**Phase 4: Advanced Features 🔜**
- Authentication
- Rate limiting
- Caching
- WebSockets
