import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.utils import create_tables

from app.auth.router import auth_router
from app.admin.router import admin_router
from app.panel.router import panel_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    

app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(panel_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.get("/")
# async def root():
#     return "Hello world!"