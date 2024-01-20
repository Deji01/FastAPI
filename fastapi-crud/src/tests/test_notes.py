from app.api import crud

import json
from datetime import datetime

def test_create_note(test_app, monkeypatch):
    test_request_payload = {"title": "something", "description": "something else"}
    date_now = datetime.now()
    test_response_payload = {
        "id": "SpUPqRU_m8svdtLTV2kEy",
        "title": "something",
        "description": "something else",
        "created_at": date_now.strftime('%Y-%m-%dT%H:%M:%S.%f')
    }

    async def mock_post(payload):
        return {
        "id": "SpUPqRU_m8svdtLTV2kEy",
        "title": "something",
        "description": "something else",
        "created_at": date_now
    }

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        "/notes/",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_app):
    response = test_app.post("/notes/", content=json.dumps({"title": "something"}))
    assert response.status_code == 422

def test_read_note(test_app, monkeypatch):
     test_data = {
        "id": "SpUPqRU_m8svdtLTV2kEy",
        "title": "something",
        "description": "something else",
    }
     
     async def mock_get(id):
         return test_data
     
     monkeypatch.setattr(crud, "get", mock_get)

     response = test_app.get("/notes/SpUPqRU_m8svdtLTV2kEy")
     assert response.status_code == 200
     assert response.json() == test_data

def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None
    
    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/099")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"