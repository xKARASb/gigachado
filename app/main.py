from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db.utils import create_tables
from .auth.router import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    

app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
# app.get("/")
# async def root():
#     return "Hello world!"