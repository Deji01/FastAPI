from .api import notes, ping, root
from .db import engine

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(_: FastAPI):
    await SQLModel.metadata.create_all(engine)
    yield


USE_LIFESPAN = True

app = FastAPI(lifespan=lifespan if USE_LIFESPAN else None)

app.include_router(root.router)
app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
