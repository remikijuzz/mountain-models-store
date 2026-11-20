import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.exceptions import BusinessRuleError, DuplicateEntityError, EntityNotFoundError

logger = logging.getLogger("app.main")


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(EntityNotFoundError, handle_not_found)
    app.add_exception_handler(BusinessRuleError, handle_business_rule)
    app.add_exception_handler(DuplicateEntityError, handle_duplicate)
    app.add_exception_handler(RequestValidationError, handle_validation)
    app.add_exception_handler(HTTPException, handle_http_error)
    app.add_exception_handler(Exception, handle_unexpected_error)


def error_response(status_code: int, exc: Exception, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": type(exc).__name__, "detail": detail},
    )


async def handle_not_found(request: Request, exc: EntityNotFoundError) -> JSONResponse:
    return error_response(status.HTTP_404_NOT_FOUND, exc, str(exc))


async def handle_business_rule(request: Request, exc: BusinessRuleError) -> JSONResponse:
    return error_response(status.HTTP_409_CONFLICT, exc, str(exc))


async def handle_duplicate(request: Request, exc: DuplicateEntityError) -> JSONResponse:
    return error_response(status.HTTP_409_CONFLICT, exc, str(exc))


async def handle_validation(request: Request, exc: RequestValidationError) -> JSONResponse:
    messages = []
    for error in exc.errors():
        field = ".".join(str(part) for part in error["loc"])
        messages.append(f"{field}: {error['msg']}")
    return error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY, exc, " | ".join(messages)
    )


async def handle_http_error(request: Request, exc: HTTPException) -> JSONResponse:
    response = error_response(exc.status_code, exc, str(exc.detail))
    if exc.headers:
        response.headers.update(exc.headers)
    return response


async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Nieobsłużony błąd żądania", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "InternalServerError", "detail": "Wewnętrzny błąd serwera."},
    )
