from fastapi import FastAPI

from app.routers.votes import vote

from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "https://www.google.com",
    # "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "My api of course"}
