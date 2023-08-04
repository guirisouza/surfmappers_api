import http

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from apps.helpers.exception import (
    HTTPError,
)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPError)
    async def http_error_handler(_: Request, exc: HTTPError) -> JSONResponse:
        headers = getattr(exc, "headers", None)
        return JSONResponse(
            {
                "error_code": exc.error_code,
                "error_message": exc.error_message,
            },
            status_code=exc.status_code,
            headers=headers,
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        _: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": http.HTTPStatus(  # pylint: disable=E1101
                    HTTP_422_UNPROCESSABLE_ENTITY,
                ).name.lower(),
                "error_message": jsonable_encoder(exc.errors()),
            },
        )
