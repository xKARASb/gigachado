from contextlib import asynccontextmanager
from fastapi import FastAPI
# from .repository.db.utils import create_tables
from .db.utils import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    

app = FastAPI(lifespan=lifespan)

app.get("/")
async def root():
    return "Hello world!"