from .models import NoteSchema, NoteDB
from ..db import get_session

from datetime import datetime

from fastapi import Depends
from nanoid import generate
from sqlmodel import Session, select


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

async def get(id: str, session: Session = Depends(get_session)):
    query = select(NoteDB).where(NoteDB.id == id)
    note = await session.exec(query).first()
    return note

async def get_all(session: Session = Depends(get_session)):
    query = select(NoteDB)
    notes = await session.exec(query).all()
    return notes

async def put(id: str, payload: NoteSchema, session: Session = Depends(get_session)):
    query = select(NoteDB).where(NoteDB.id == id)
    note = await session.exec(query).one()
    if payload.title:
        note.title = payload.title
    if payload.description:
        note.description = payload.description
    session.add(note)
    session.commit()
    session.refresh(note)
    return note