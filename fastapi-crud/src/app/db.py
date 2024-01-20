import os

from sqlmodel import Session, create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

# Database connection
engine = create_engine(DATABASE_URL)


# databases query builder
def get_session():
    "Query database(s) with session"
    with Session(engine) as session:
        yield session
