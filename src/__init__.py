from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting...")
    await init_db()
    yield

    print(f"Server has been stopped")


__version__ = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for book review web service",
    version=__version__,
    lifespan=life_span,
)

app.include_router(book_router, prefix=f"/api/{__version__}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{__version__}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{__version__}/review", tags=["reviews"])
