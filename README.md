# AdvRAG - Advanced RAG Backend System

A production-grade Retrieval-Augmented Generation (RAG) chatbot system with document ingestion pipeline, built with FastAPI, Supabase, and LangChain.

## 🚀 Features

- ✅ **Async Architecture** - Built for high concurrency and performance
- ✅ **Database Management** - PostgreSQL with connection pooling and retry logic
- ✅ **Chat Sessions** - Full CRUD API for managing chat sessions
- ✅ **Production-Ready** - Comprehensive error handling, logging, and health checks
- 🔜 **Document Ingestion** - Coming soon: Upload and process documents
- 🔜 **RAG Pipeline** - Coming soon: Query documents with LLM assistance

## 📋 Prerequisites

- Python 3.11+
- [Supabase Account](https://supabase.com) (free tier available)
- [OpenAI API Key](https://platform.openai.com)
- Poetry or pip for dependency management

## ⚡ Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Make the script executable
chmod +x quickstart.sh

# Run the quick start script
./quickstart.sh
```

### Option 2: Manual Setup

```bash
# 1. Clone the repository
cd /path/to/advRAG

# 2. Install dependencies
pip install -e .
# OR using Poetry:
poetry install

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# 4. Initialize database
python backend/scripts/init_db.py

# 5. Run the application
cd backend
python -m app.main
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

**Required:**
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key

**Optional (have defaults):**
- `DATABASE_POOL_SIZE` - Connection pool size (default: 20)
- `DB_MAX_RETRIES` - Max connection retries (default: 3)
- `LOG_LEVEL` - Logging level (default: INFO)

See `.env.example` for all available options.

## 📚 Documentation

- **[API Reference](API.md)** - Complete API endpoints and examples
- **[Development Guide](DEVELOPMENT.md)** - Architecture, setup, and implementation
- **[Architecture Diagram](ARCHITECTURE_DIAGRAM.md)** - System design and component interactions
- **[Documentation Index](DOCS_INDEX.md)** - Navigate all documentation
- **Interactive API Docs** - http://localhost:8000/docs (when running)

## 🌐 API Endpoints & Testing

### 🎯 Interactive API Documentation (Swagger)

**Once running, access the interactive API docs:**
```
http://localhost:8000/docs
```

**Features:**
- ✅ Try all endpoints directly in the browser
- ✅ See request/response examples
- ✅ View validation rules
- ✅ Auto-generated code samples
- ✅ Complete API reference

See **[SWAGGER_SETUP.md](SWAGGER_SETUP.md)** for detailed guide.

### 📋 Quick API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/sessions` | POST | Create new session |
| `/api/v1/sessions/{id}` | GET | Get session by ID |
| `/api/v1/sessions` | GET | List sessions (with filters) |
| `/api/v1/sessions/{id}` | PATCH | Update session |
| `/api/v1/sessions/{id}` | DELETE | Delete session |
| `/api/v1/health` | GET | Health check |

### 💻 Example: Create Session

**Using Swagger UI:** http://localhost:8000/docs
1. Click on `POST /api/v1/sessions`
2. Click "Try it out"
3. Edit the request body
4. Click "Execute"

**Using cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "title": "My Chat Session"}'
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_123",
  "title": "My Chat Session",
  "status": "active",
  "message": "hello! upload docs for me to Index"
}
```

See **[API.md](API.md)** for complete endpoint documentation.

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│      FastAPI Application            │
│  • Async request handling           │
│  • Database lifecycle management    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         API Layer                   │
│  • REST endpoints                   │
│  • Request/response validation      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       Service Layer                 │
│  • Business logic                   │
│  • Data transformation              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Database Layer                 │
│  • Connection pooling               │
│  • Retry logic with backoff         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Supabase PostgreSQL              │
└─────────────────────────────────────┘
```

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/

# Run specific test file
pytest backend/tests/test_sessions.py
```

## 📦 Project Structure

```
advRAG/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── db/           # Database client & manager
│   │   ├── models/       # SQLAlchemy models & schemas
│   │   ├── services/     # Business logic
│   │   ├── config.py     # Configuration
│   │   └── main.py       # Application entry point
│   ├── scripts/          # Utility scripts
│   └── tests/            # Test suite
├── .env.example          # Environment template
├── pyproject.toml        # Dependencies
└── README.md             # This file
```

## 🔥 Key Features

### Async Database Management
- Connection pooling for efficient resource use
- Automatic retry with exponential backoff
- Health monitoring and graceful degradation

### Error Handling
- Comprehensive exception handling
- Structured error responses
- Proper HTTP status codes

### Logging
- Structured logging throughout
- Configurable log levels
- Request/response tracking

### Production-Ready
- Environment-based configuration
- Database connection resilience
- Health check endpoints
- CORS support

## 🚧 Roadmap

### Phase 1: Foundation ✅ Complete
- [x] Database setup with Supabase
- [x] Chat session management
- [x] API endpoints
- [x] Error handling and logging

### Phase 2: Document Ingestion 🔜 Next
- [ ] File upload API
- [ ] Document parsing (PDF, DOCX, TXT, MD)
- [ ] Text chunking with LangChain
- [ ] Embedding generation with OpenAI
- [ ] Vector storage in Supabase

### Phase 3: RAG Implementation 🔜
- [ ] Vector similarity search
- [ ] Context retrieval
- [ ] LLM query endpoint
- [ ] Streaming responses
- [ ] Chat history

### Phase 4: Advanced Features 🔜
- [ ] User authentication
- [ ] Rate limiting
- [ ] Caching with Redis
- [ ] Background processing with Celery
- [ ] WebSocket for real-time chat

## 🤝 Contributing

This is a production-grade implementation focusing on:
- Clean architecture
- Type safety with Pydantic v2
- Async operations
- Comprehensive error handling
- Production best practices

## 📄 License

MIT

## 🆘 Troubleshooting

### Database Connection Issues
1. Verify Supabase credentials in `.env`
2. Check your network connectivity
3. Use the health check: `GET /api/v1/health`

### Import Errors
1. Ensure all dependencies are installed: `pip install -e .`
2. Activate virtual environment
3. Check Python version: `python --version` (should be 3.11+)

### Environment Variables
1. Ensure `.env` file exists in project root
2. Check for typos in variable names
3. No trailing spaces in values

For more help, see [SETUP.md](SETUP.md)

## 📞 Support

- Check logs for detailed error messages
- Use `/docs` endpoint for API documentation
- Review `IMPLEMENTATION_SUMMARY.md` for technical details

---

**Status:** ✅ Phase 1 Complete - Chat Session Management
**Next:** 🔜 Phase 2 - Document Ingestion Pipeline