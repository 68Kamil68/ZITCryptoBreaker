from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project.celery_utils import create_celery
from pydantic import BaseModel

from . import tasks


class HashData(BaseModel):
    hash: str
    email: str
    wordlist: str | None


def create_app() -> FastAPI:
    app = FastAPI()

    # do this before loading routes
    app.celery_app = create_celery()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/break-hash", response_model=HashData)
    async def break_hash(hash_data: HashData):
        tasks.break_hash.delay(hash_data.hash, hash_data.email, hash_data.wordlist)
        return hash_data

    return app
