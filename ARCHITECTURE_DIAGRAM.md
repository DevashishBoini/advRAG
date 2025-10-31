# Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  (Browser, Mobile App, API Client, cURL, Python requests)       │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP/HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI APPLICATION                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Middleware Stack                        │  │
│  │  • CORS Middleware (Cross-Origin Resource Sharing)        │  │
│  │  • Logging Middleware (Request/Response tracking)         │  │
│  │  • Exception Handlers (Global error handling)             │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     API ROUTER                             │  │
│  │  /api/v1/health    → Health Check                         │  │
│  │  /api/v1/sessions  → Session Management                   │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API LAYER                                 │
│  app/api/routes/                                                 │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │  health.py   │  │ sessions.py  │                            │
│  │              │  │              │                            │
│  │ GET /health  │  │ POST    /    │                            │
│  │              │  │ GET     /{id}│                            │
│  │              │  │ GET     /    │                            │
│  │              │  │ PATCH   /{id}│                            │
│  │              │  │ DELETE  /{id}│                            │
│  └──────────────┘  └──────────────┘                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      HANDLER LAYER                               │
│  app/api/handlers/                                               │
│  ┌─────────────────────┐  ┌──────────────────────────────────┐ │
│  │ health_handlers.py  │  │   session_handlers.py            │ │
│  │                     │  │                                  │ │
│  │ • handle_health()   │  │ • handle_create_session()        │ │
│  │                     │  │ • handle_get_session()           │ │
│  │                     │  │ • handle_list_sessions()         │ │
│  │                     │  │ • handle_update_session()        │ │
│  │                     │  │ • handle_delete_session()        │ │
│  └─────────────────────┘  └──────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  VALIDATION LAYER                                │
│  app/utils/validators.py                                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              InputValidator (Static Methods)               │  │
│  │                                                            │  │
│  │  • validate_title()      → SQL injection, length, chars   │  │
│  │  • validate_user_id()    → Character validation, security │  │
│  │  • validate_status()     → Whitelist validation           │  │
│  │  • validate_metadata()   → Size, structure, type checks   │  │
│  │  • validate_pagination() → Limit/offset validation        │  │
│  │  • validate_uuid()       → UUID format validation         │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PYDANTIC SCHEMAS                               │
│  app/models/schemas.py                                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  SessionCreateRequest  → Validates create payload         │  │
│  │  SessionUpdateRequest  → Validates update payload         │  │
│  │  SessionResponse       → Standardized response format     │  │
│  │  ErrorResponse         → Error response format            │  │
│  │                                                            │  │
│  │  (Uses @field_validator to call InputValidator methods)   │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                                │
│  app/services/                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              session_service.py                            │  │
│  │                                                            │  │
│  │  • create_session()   → Business logic for creation       │  │
│  │  • get_session()      → Retrieve single session           │  │
│  │  • list_sessions()    → List with filters/pagination      │  │
│  │  • update_session()   → Update session fields             │  │
│  │  • delete_session()   → Soft/hard delete                  │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                                │
│  app/db/                                                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   manager.py                               │  │
│  │                                                            │  │
│  │  DatabaseManager:                                          │  │
│  │  • Connection pooling (default: 20)                       │  │
│  │  • Async session management                               │  │
│  │  • Retry with exponential backoff (max: 3)               │  │
│  │  • Health monitoring                                      │  │
│  │  • Graceful shutdown                                      │  │
│  │                                                            │  │
│  │  Methods:                                                  │  │
│  │  • get_session() → Context manager for DB sessions        │  │
│  │  • execute_with_retry() → Retry wrapper for queries       │  │
│  │  • check_health() → Database connectivity check           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    client.py                               │  │
│  │                                                            │  │
│  │  • SQLAlchemy engine configuration                        │  │
│  │  • Async connection setup                                 │  │
│  │  • Session factory                                        │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ORM LAYER                                   │
│  app/models/session.py                                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              ChatSession (SQLAlchemy Model)                │  │
│  │                                                            │  │
│  │  Fields:                                                   │  │
│  │  • id (UUID, PK)                                          │  │
│  │  • user_id (VARCHAR 255)                                  │  │
│  │  • title (VARCHAR 500)                                    │  │
│  │  • status (VARCHAR 50)                                    │  │
│  │  • is_active (BOOLEAN)                                    │  │
│  │  • metadata (JSONB)                                       │  │
│  │  • created_at (TIMESTAMPTZ)                               │  │
│  │  • updated_at (TIMESTAMPTZ)                               │  │
│  │                                                            │  │
│  │  Indexes:                                                  │  │
│  │  • idx_chat_sessions_user_id                              │  │
│  │  • idx_chat_sessions_status                               │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATABASE (PostgreSQL)                          │
│                      Supabase Hosted                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    chat_sessions                           │  │
│  │                                                            │  │
│  │  • Persistent storage                                     │  │
│  │  • ACID transactions                                      │  │
│  │  • Indexed queries                                        │  │
│  │  • JSONB support for metadata                             │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow

### Example: Create Session Request

```
1. Client sends POST /api/v1/sessions
   ↓
2. CORS Middleware validates origin
   ↓
3. Logging Middleware logs request
   ↓
4. FastAPI Router routes to sessions.create_session()
   ↓
5. Pydantic validates request body (SessionCreateRequest)
   • Basic validation: types, max_length, optional fields
   • Custom validation: calls InputValidator methods
   ↓
6. Handler calls session_service.create_session()
   ↓
7. Service Layer processes business logic
   ↓
8. DatabaseManager.get_session() provides DB session
   ↓
9. SQLAlchemy ORM creates ChatSession model
   ↓
10. Query executed with parameterization (SQL injection safe)
    ↓
11. Database persists record and returns result
    ↓
12. Service returns ChatSession object
    ↓
13. Handler converts to SessionResponse (Pydantic)
    ↓
14. FastAPI serializes response to JSON
    ↓
15. Logging Middleware logs response
    ↓
16. Client receives 201 Created with JSON body
```

## Error Flow

```
Exception occurs anywhere in stack
   ↓
Global Exception Handler catches it
   ↓
Maps to appropriate ErrorResponse
   ↓
Returns JSON with:
   • error: Human-readable message
   • detail: Specific details
   • timestamp: ISO 8601
   • HTTP status code (400/404/500/503)
```

## Component Interactions

```
┌──────────────┐
│   Routes     │ ← Define endpoints, path/query params
└──────┬───────┘
       │ delegates to
       ▼
┌──────────────┐
│   Handlers   │ ← Orchestrate flow, call services
└──────┬───────┘
       │ calls
       ▼
┌──────────────┐
│   Services   │ ← Business logic, data transformation
└──────┬───────┘
       │ uses
       ▼
┌──────────────┐
│  DB Manager  │ ← Connection management, retry logic
└──────┬───────┘
       │ provides sessions to
       ▼
┌──────────────┐
│ ORM (Models) │ ← Data models, query building
└──────┬───────┘
       │ executes on
       ▼
┌──────────────┐
│  PostgreSQL  │ ← Data persistence
└──────────────┘
```

## Security Layers

```
┌─────────────────────────────────────┐
│  Layer 1: FastAPI Type Validation   │ ← Basic type safety
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  Layer 2: Pydantic Constraints      │ ← max_length, ge, le, Optional
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  Layer 3: Custom Validators         │ ← SQL injection, char validation
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  Layer 4: SQLAlchemy Parameterized  │ ← Query parameterization
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  Layer 5: Database Constraints      │ ← DB-level validation
└─────────────────────────────────────┘
```

## Configuration Flow

```
┌──────────────┐
│ .env file    │ → Environment variables
└──────┬───────┘
       │ loaded by
       ▼
┌──────────────┐
│ config.py    │ → Settings (Pydantic BaseSettings)
└──────┬───────┘
       │ used by
       ▼
┌──────────────────────────────────┐
│ • main.py (app configuration)    │
│ • db/client.py (DB connection)   │
│ • services (business logic)      │
└──────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────┐
│         Production Setup             │
└─────────────────────────────────────┘

┌──────────────┐     ┌─────────────────┐
│ Load Balancer│ ──→ │ FastAPI Instance│
└──────────────┘     │    (Uvicorn)    │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │  Connection Pool│
                     │   (20 conns)    │
                     └────────┬────────┘
                              │
                     ┌────────▼────────┐
                     │    Supabase     │
                     │   PostgreSQL    │
                     └─────────────────┘
```

## Future Extensions

```
┌─────────────────────────────────────────────────────────┐
│                    Phase 2: RAG Pipeline                 │
└─────────────────────────────────────────────────────────┘

Document Upload → Parser → Chunker → Embeddings → Vector Store
                                                       ↓
Query → Retriever → Context Assembly → LLM → Response
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **API Framework** | FastAPI 0.104+ |
| **Runtime** | Python 3.11+ |
| **ORM** | SQLAlchemy 2.0 (Async) |
| **Validation** | Pydantic v2 |
| **Database** | PostgreSQL (Supabase) |
| **Server** | Uvicorn (ASGI) |
| **Testing** | Pytest |
| **Documentation** | Swagger/OpenAPI (built-in) |

## Key Design Principles

1. **Separation of Concerns** - Each layer has a single responsibility
2. **Dependency Injection** - Global db_manager, no instance storage
3. **Defense in Depth** - Multiple validation layers
4. **Async-First** - All I/O operations are async
5. **Fail-Fast** - Validation at API boundary
6. **Graceful Degradation** - Retry logic, health checks
7. **Production-Ready** - Logging, monitoring, error handling
