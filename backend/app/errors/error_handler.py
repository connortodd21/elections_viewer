from typing import Tuple
from werkzeug.http import HTTP_STATUS_CODES

from app.api import bp


def error_response(status_code: int, message=None) -> Tuple[dict, int]:
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code