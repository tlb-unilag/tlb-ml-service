import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import detection
from routers import auth
from database import engine, Base
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(detection.router)
