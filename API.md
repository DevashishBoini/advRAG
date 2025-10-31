# API Reference

## Base URL
```
http://localhost:8000/api/v1
```

## Endpoints

### Health Check
```http
GET /api/v1/health
```

**Response 200:**
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0",
  "timestamp": "2025-11-01T12:00:00Z"
}
```

---

### Create Session
```http
POST /api/v1/sessions
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "user_123",           // Optional, max 255 chars
  "title": "My Chat Session",      // Optional, 1-500 chars
  "metadata": {                     // Optional, max 10KB
    "source": "web",
    "priority": 1
  }
}
```

**Response 201:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_123",
  "title": "My Chat Session",
  "status": "active",
  "is_active": true,
  "metadata": {"source": "web", "priority": 1},
  "created_at": "2025-11-01T12:00:00Z",
  "updated_at": "2025-11-01T12:00:00Z",
  "message": "hello! upload docs for me to Index"
}
```

**Response 400 (Validation Error):**
```json
{
  "error": "Validation failed",
  "detail": "Title must be between 1 and 500 characters",
  "timestamp": "2025-11-01T12:00:00Z"
}
```

---

### Get Session
```http
GET /api/v1/sessions/{session_id}
```

**Parameters:**
- `session_id` (path) - UUID of the session

**Response 200:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_123",
  "title": "My Chat Session",
  "status": "active",
  "is_active": true,
  "metadata": {},
  "created_at": "2025-11-01T12:00:00Z",
  "updated_at": "2025-11-01T12:00:00Z",
  "message": "Session retrieved successfully"
}
```

**Response 404:**
```json
{
  "error": "Session not found",
  "detail": "Session with ID 550e8400-e29b-41d4-a716-446655440000 not found",
  "timestamp": "2025-11-01T12:00:00Z"
}
```

---

### List Sessions
```http
GET /api/v1/sessions?user_id={user_id}&limit={limit}&offset={offset}
```

**Query Parameters:**
- `user_id` (optional) - Filter by user ID, max 255 chars
- `limit` (optional) - Results per page, 1-100, default: 50
- `offset` (optional) - Pagination offset, ≥0, default: 0

**Response 200:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user_123",
    "title": "Session 1",
    "status": "active",
    "is_active": true,
    "metadata": {},
    "created_at": "2025-11-01T12:00:00Z",
    "updated_at": "2025-11-01T12:00:00Z",
    "message": "Session retrieved successfully"
  }
]
```

---

### Update Session
```http
PATCH /api/v1/sessions/{session_id}
Content-Type: application/json
```

**Parameters:**
- `session_id` (path) - UUID of the session

**Request Body (all fields optional):**
```json
{
  "title": "Updated Title",                        // 1-500 chars
  "status": "completed",                          // active|completed|archived|paused
  "is_active": false,                             // boolean
  "metadata": {"updated": true, "version": 2}     // max 10KB
}
```

**Response 200:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user_123",
  "title": "Updated Title",
  "status": "completed",
  "is_active": false,
  "metadata": {"updated": true, "version": 2},
  "created_at": "2025-11-01T12:00:00Z",
  "updated_at": "2025-11-01T12:30:00Z",
  "message": "Session updated successfully"
}
```

**Response 404:**
```json
{
  "error": "Session not found",
  "detail": "Session with ID 550e8400-e29b-41d4-a716-446655440000 not found",
  "timestamp": "2025-11-01T12:00:00Z"
}
```

---

### Delete Session
```http
DELETE /api/v1/sessions/{session_id}
```

**Parameters:**
- `session_id` (path) - UUID of the session

**Response 204:**
No content

**Response 404:**
```json
{
  "error": "Session not found",
  "detail": "Session with ID 550e8400-e29b-41d4-a716-446655440000 not found",
  "timestamp": "2025-11-01T12:00:00Z"
}
```

---

## Response Standards

### Success Responses
All successful responses include:
- `200` - OK (GET, PATCH)
- `201` - Created (POST)
- `204` - No Content (DELETE)
- ISO 8601 timestamps
- Consistent field naming (snake_case)
- `message` field for user feedback

### Error Responses
All error responses include:
- `error` - Human-readable error message
- `detail` - Specific error details
- `timestamp` - ISO 8601 timestamp
- Appropriate HTTP status codes

**Status Codes:**
- `400` - Bad Request (validation errors)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error (unexpected errors)
- `503` - Service Unavailable (database connection issues)

---

## Validation Rules

### Field Constraints

**user_id:**
- Type: String
- Max length: 255 characters
- Allowed: Alphanumeric + `_-.@`
- Validation: SQL injection checks, character validation

**title:**
- Type: String
- Length: 1-500 characters
- Allowed: Printable characters only
- Validation: SQL injection checks, min/max length

**status:**
- Type: String (enum)
- Allowed values: `active`, `completed`, `archived`, `paused`
- Default: `active`

**is_active:**
- Type: Boolean
- Default: `true`

**metadata:**
- Type: Object (JSON)
- Max size: 10 KB
- Max key length: 100 characters
- Allowed value types: string, number, boolean, null
- No nested objects allowed

**pagination:**
- `limit`: 1-100 (default: 50)
- `offset`: ≥0 (default: 0)

### Security

**SQL Injection Protection:**
- Pattern detection for common SQL injection attempts
- Parameterized queries via SQLAlchemy
- Input sanitization
- Character validation

**Patterns Blocked:**
`UNION`, `SELECT`, `DROP`, `DELETE`, `INSERT`, `UPDATE`, `--`, `;--`, `xp_`, `sp_`, `EXEC`, `EXECUTE`, `SCRIPT`, `JAVASCRIPT`, `ONERROR`, `<script>`, etc.

---

## Examples

### cURL Examples

**Create Session:**
```bash
curl -X POST http://localhost:8000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "title": "My Session"}'
```

**Get Session:**
```bash
curl http://localhost:8000/api/v1/sessions/550e8400-e29b-41d4-a716-446655440000
```

**List Sessions:**
```bash
curl "http://localhost:8000/api/v1/sessions?user_id=user_123&limit=10"
```

**Update Session:**
```bash
curl -X PATCH http://localhost:8000/api/v1/sessions/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

**Delete Session:**
```bash
curl -X DELETE http://localhost:8000/api/v1/sessions/550e8400-e29b-41d4-a716-446655440000
```

### Python Examples

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Create session
response = requests.post(
    f"{BASE_URL}/sessions",
    json={"user_id": "user_123", "title": "My Session"}
)
session = response.json()

# Get session
session_id = session["id"]
response = requests.get(f"{BASE_URL}/sessions/{session_id}")

# List sessions
response = requests.get(
    f"{BASE_URL}/sessions",
    params={"user_id": "user_123", "limit": 10}
)
sessions = response.json()

# Update session
response = requests.patch(
    f"{BASE_URL}/sessions/{session_id}",
    json={"status": "completed"}
)

# Delete session
response = requests.delete(f"{BASE_URL}/sessions/{session_id}")
```

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can:
- View all endpoints
- See request/response schemas
- Test API calls directly
- View validation rules
