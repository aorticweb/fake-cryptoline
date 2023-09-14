from requests import Response

from bot.exceptions import DataSourceException


def validate_api_request_status_code(resp: Response):
    if resp.status_code > 299:
        raise DataSourceException(resp.status_code, resp.text)
