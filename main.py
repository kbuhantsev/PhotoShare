from fastapi import FastAPI, Depends, HTTPException

from src.auth.router import router as auth_router
from src.photos.router import router as photos_router
from src.tags.router import router as tags_router
from src.user.router import router as user_router
from src.comments.router import router as comments_router
from src.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
app = FastAPI()

app.include_router(auth_router, prefix="/api")
app.include_router(photos_router, prefix="/api")
app.include_router(tags_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(comments_router, prefix="/api")


@app.on_event("startup")
async def startup():
    print("Starting up...")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/api/healthchecker")
# async def healthchecker():
#     return {"message": "Welcome to FastAPI"}
#

@app.get("/api/healthchecker_db")
async def healthchecker_db(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

