from fastapi import FastAPI
from .books.routers import book_router
from src.auth.router import auth_router
from contextlib import asynccontextmanager
from .db.main import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print("server is starting ...")
    await init_db()
    yield 
    print("server stopped ")

version = "v1"
app = FastAPI(
    title="bookly",
    description = "a rest api for book management system",
    version=version,
    #lifespan=life_span,
)

app.include_router(book_router,prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router,prefix=f"/api/{version}/auth", tags=["auth"])