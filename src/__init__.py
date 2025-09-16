from fastapi import FastAPI
from .books.routers import book_router

version = "v1"
app = FastAPI(
    title="bookly",
    description = "a rest api for book management system",
    version=version
)

app.include_router(book_router,prefix=f"/api/{version}/books", tags=["books"])