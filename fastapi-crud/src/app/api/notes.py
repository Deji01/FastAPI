from . import crud
from .models import NoteDB, NoteSchema

from fastapi import APIRouter, HTTPException, status
from typing import List

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    note = await crud.post(payload)

    result = {
        "id": note["id"],
        "title": payload.title,
        "description": payload.description,
        "created_at": note["created_at"],
    }
    return result


@router.get("/{id}/", response_model=NoteDB, status_code=200)
async def get_note(id: str):
    note = await crud.get(id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.get("/", response_model=List[NoteDB], status_code=200)
async def read_all_notes():
    notes = await crud.get_all()
    if not notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notes not found"
        )
    return notes
