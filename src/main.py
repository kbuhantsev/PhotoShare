from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.photos.router import router as photos_router
from src.tags.router import router as tags_router

app = FastAPI()

app.include_router(auth_router, prefix="/api")
app.include_router(photos_router, prefix="/api")
app.include_router(tags_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
async def healthchecker():
    return {"message": "Welcome to FastAPI"}
