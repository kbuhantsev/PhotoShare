from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.router import router as auth_router
from src.comments.router import router as comments_router
from src.database import get_db
from src.photos.router import router as photos_router
from src.tags.router import router as tags_router
from src.user.router import router as user_router
from src.rating.router import router as rating_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    yield
    print("Closing application...")


app = FastAPI(lifespan=lifespan)

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "dist" ), name="static")
app.mount("/assets", StaticFiles(directory=BASE_DIR / "dist" / "assets"), name="assets")

origins = [
    # "http://localhost",
    # "http://localhost:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(photos_router, prefix="/api")
app.include_router(tags_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(rating_router, prefix="/api")


@app.get("/")
async def root():
    content = Path(BASE_DIR / "dist" / "index.html").read_text()
    return HTMLResponse(content=content, status_code=200)


@app.get("/api/healthchecker")
async def healthchecker_db(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
