from functools import wraps
from typing import Callable

from fastapi import (
    Request,
    Response,
)
from fastapi.routing import APIRoute

from fastapi_localization.response import TranslateJsonResponse


class LocalizationRoute(APIRoute):
    """
    Route that localizes response
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def translate(func):
            """ Endpoint wrapper that does result translation """

            @wraps(func)
            async def wrapper(*args, **kwargs) -> TranslateJsonResponse:
                response_data = await func(*args, **kwargs)
                return TranslateJsonResponse(content=response_data.model_dump())

            return wrapper

        self.endpoint = translate(self.endpoint)


    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)
            if isinstance(response, TranslateJsonResponse):
                return response.translate_content(request.state.gettext)
            return response
        return custom_route_handler
