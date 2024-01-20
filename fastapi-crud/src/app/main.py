from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api import notes, ping, root
from .db import engine, database, metadata

metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


USE_LIFESPAN = True

app = FastAPI(lifespan=lifespan if USE_LIFESPAN else None)

app.include_router(root.router)
app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
