from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.error_handlers import register_error_handlers
from app.routers import customers, mountain_models, orders
from app.schemas.error import ErrorResponse



@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        engine.dispose()


app = FastAPI(
    title="Mountain Models Store",
    lifespan=lifespan,
    responses={
        400: {"model": ErrorResponse, "description": "Błąd odczytu żądania"},
        422: {"model": ErrorResponse, "description": "Błąd walidacji żądania"},
        500: {"model": ErrorResponse, "description": "Wewnętrzny błąd serwera"},
    },
)

app.include_router(customers.router)
app.include_router(mountain_models.router)
app.include_router(orders.router)
register_error_handlers(app)
