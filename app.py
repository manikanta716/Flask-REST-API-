"""
Flask Notes API
A RESTful API for managing notes with full CRUD operations.
"""

from flask import Flask, jsonify, request, abort
from datetime import datetime, timezone
import uuid

app = Flask(__name__)

# In-memory store (swap for a real DB in production)
notes: dict[str, dict] = {}


# ── Helpers ──────────────────────────────────────────────────────────────────

def note_or_404(note_id: str) -> dict:
    note = notes.get(note_id)
    if not note:
        abort(404, description=f"Note '{note_id}' not found.")
    return note


def validate_body(required_fields: list[str]) -> dict:
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Request body must be valid JSON.")
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            abort(400, description=f"Missing or empty field: '{field}'")
    return data


# ── Error handlers ────────────────────────────────────────────────────────────

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def handle_error(e):
    return jsonify({"error": str(e.description)}), e.code


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def index():
    return jsonify({
        "name": "Flask Notes API",
        "version": "1.0",
        "endpoints": {
            "GET    /notes":              "List all notes",
            "POST   /notes":              "Create a note",
            "GET    /notes/<id>":         "Get a note",
            "PUT    /notes/<id>":         "Replace a note",
            "PATCH  /notes/<id>":         "Update a note",
            "DELETE /notes/<id>":         "Delete a note",
            "GET    /notes/search?q=...": "Search notes",
        }
    })


@app.get("/notes")
def list_notes():
    tag = request.args.get("tag")
    result = list(notes.values())
    if tag:
        result = [n for n in result if tag in n.get("tags", [])]
    result.sort(key=lambda n: n["updated_at"], reverse=True)
    return jsonify({"count": len(result), "notes": result})


@app.post("/notes")
def create_note():
    data = validate_body(["title", "content"])
    note = {
        "id": str(uuid.uuid4()),
        "title": data["title"].strip(),
        "content": data["content"].strip(),
        "tags": data.get("tags", []),
                "created_at": datetime.now(timezone.utc).isoformat() + "Z",
                "updated_at": datetime.now(timezone.utc).isoformat() + "Z",
    }
    notes[note["id"]] = note
    return jsonify(note), 201


@app.get("/notes/search")
def search_notes():
    q = request.args.get("q", "").lower().strip()
    if not q:
        abort(400, description="Query parameter 'q' is required.")
    results = [
        n for n in notes.values()
        if q in n["title"].lower() or q in n["content"].lower()
    ]
    return jsonify({"query": q, "count": len(results), "notes": results})


@app.get("/notes/<note_id>")
def get_note(note_id: str):
    return jsonify(note_or_404(note_id))


@app.put("/notes/<note_id>")
def replace_note(note_id: str):
    note = note_or_404(note_id)
    data = validate_body(["title", "content"])
    note.update({
        "title": data["title"].strip(),
        "content": data["content"].strip(),
        "tags": data.get("tags", []),
                "updated_at": datetime.now(timezone.utc).isoformat() + "Z",
    })
    return jsonify(note)


@app.patch("/notes/<note_id>")
def update_note(note_id: str):
    note = note_or_404(note_id)
    data = request.get_json(silent=True) or {}
    if not data:
        abort(400, description="Request body must be valid JSON.")

    if "title" in data:
        note["title"] = data["title"].strip()
    if "content" in data:
        note["content"] = data["content"].strip()
    if "tags" in data:
        note["tags"] = data["tags"]

        note["updated_at"] = datetime.now(timezone.utc).isoformat() + "Z"
    return jsonify(note)


@app.delete("/notes/<note_id>")
def delete_note(note_id: str):
    note_or_404(note_id)
    del notes[note_id]
    return jsonify({"message": f"Note '{note_id}' deleted."})


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)
