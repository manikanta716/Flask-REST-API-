# 🗒️ Flask Notes API

A clean RESTful API built with Flask for managing notes. Great foundation for any CRUD-based backend.

## Features

- Full CRUD: Create, Read, Update, Delete notes
- `PUT` (replace) and `PATCH` (partial update) both supported
- Tag filtering and full-text search
- Clean JSON error responses
- UUID-based note IDs

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Server runs at `http://localhost:5000`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/notes` | List all notes |
| POST | `/notes` | Create a note |
| GET | `/notes/<id>` | Get a note |
| PUT | `/notes/<id>` | Replace a note |
| PATCH | `/notes/<id>` | Partially update a note |
| DELETE | `/notes/<id>` | Delete a note |
| GET | `/notes/search?q=...` | Search by title/content |

## Example Requests

```bash
# Create
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "My Note", "content": "Hello world", "tags": ["personal"]}'

# List
curl http://localhost:5000/notes

# Filter by tag
curl "http://localhost:5000/notes?tag=personal"

# Search
curl "http://localhost:5000/notes/search?q=hello"

# Partial update
curl -X PATCH http://localhost:5000/notes/<id> \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated content"}'

# Delete
curl -X DELETE http://localhost:5000/notes/<id>
```

## Notes

- Data is stored in-memory. Restart the server and it resets.
- To persist data, swap `notes: dict` for SQLite (via `flask-sqlalchemy`) or any DB.

## Requirements

- Python 3.9+
- Flask 3.x
