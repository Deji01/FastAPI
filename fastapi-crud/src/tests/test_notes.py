from app.api import crud

import json
from datetime import datetime

import pytest

def test_create_note(test_app, monkeypatch):
    test_request_payload = {"title": "something", "description": "something else"}
    date_now = datetime.now()
    test_response_payload = {
        "id": "SpUPqRU_m8svdtLTV2kEy",
        "title": "something",
        "description": "something else",
        "created_at": date_now.strftime("%Y-%m-%dT%H:%M:%S.%f"),
    }

    async def mock_post(payload):
        return {
            "id": "SpUPqRU_m8svdtLTV2kEy",
            "title": "something",
            "description": "something else",
            "created_at": date_now,
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


def test_read_all_notes(test_app, monkeypatch):
    test_data = [
        {
            "id": "SpUPqRU_m8svdtLTV2kEy",
            "title": "something",
            "description": "something else",
        },
        {
            "id": "SkUPqRU_m8svdtLTV2kEy",
            "title": "something",
            "description": "something else",
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/notes/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_note(test_app, monkeypatch):
    test_update_data = {
        "id": "SpUPqRU_m8svdtLTV2kEy",
        "title": "someone",
        "description": "someone else",
    }

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return {"id": id, **payload}

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(
        "/notes/SpUPqRU_m8svdtLTV2kEy/", content=json.dumps(test_update_data)
    )
    assert response.status_code == 200
    assert response.json() == test_update_data

@pytest.mark.parametrize(
    "id, payload, status_code", [
        ["SpUPqRU_m8svdtLTV2kEy", {}, 422], 
        ["SpUPqRU_m8svdtLTV2kEy", {"description": "bar"}, 422], 
        ["srtdfgdfdglpo_fjg", {"title": "foo", "description": "bar"}, 404],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/notes/{id}/", content=json.dumps(payload))
    assert response.status_code == status_code