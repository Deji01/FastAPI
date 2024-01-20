from datetime import datetime

from sqlmodel import SQLModel, Field


class NoteSchema(SQLModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=50)


class NoteDB(NoteSchema, table=True):
    id: str = Field(primary_key=True)
    created_at: datetime
