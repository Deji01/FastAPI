from .models import NoteSchema, NoteDB
from ..db import get_session

from datetime import datetime

from fastapi import Depends
from nanoid import generate
from sqlmodel import Session


async def post(payload: NoteSchema, session: Session = Depends(get_session)):
    note = NoteDB(
        id=generate(),
        title=payload.title,
        description=payload.description,
        created_at=datetime.now(),
    )
    await session.add(note)
    await session.commit()
    return note
