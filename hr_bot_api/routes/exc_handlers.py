import starlette.requests
from starlette.responses import JSONResponse

from hr_bot_api.exceptions import (
    ObjectNotFound,
)
from hr_bot_api.schemas.base import StatusResponseModel

from .base import app


@app.exception_handler(ObjectNotFound)
async def not_found_handler(req: starlette.requests.Request, exc: ObjectNotFound):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.eng, ru=exc.ru).model_dump(), status_code=404
    )