import gettext
import typing

from fastapi.responses import JSONResponse

from fastapi_localization.localization import prepare_content_to_translate


class TranslateJsonResponse(JSONResponse):
    """
    Response that localization content
    """
    def __init__(
            self, content: typing.Any = None,
            status_code: int = 200, *args, **kwargs,
    ):
        print('============= response init =====================')
        print(f'args: {args}')
        print(f'kwargs: {kwargs}')
        self.original_content = content
        print(f'original_content: {content} | {type(content)}')
        # print(f'name: {content["name"]} | {type(content["name"])}')

        super().__init__(content, status_code, *args, **kwargs)

    def translate_content(self, _: gettext.GNUTranslations.gettext):
        print('============= translate_content =====================')

        print(f'original_content: {self.original_content} | {type(self.original_content)}')
        # print(f'name: {self.original_content["name"]} | {type(self.original_content["name"])}')

        content = prepare_content_to_translate(
            self.original_content, _
        )
        return TranslateJsonResponse(
            content, status_code=self.status_code,
            background=self.background
        )
