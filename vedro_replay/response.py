import json
from typing import Dict, List
from requests_toolbelt.multipart import decoder


class Response:
    def __init__(self, status: int, headers: Dict, body, request_url: str) -> None:
        self.status = status
        self.headers = headers
        self.body = body
        self.request_url = request_url

    def __repr__(self) -> str:
        r = f'REQUEST: {self.request_url}\n'
        r += f'STATUS CODE: {self.status}'
        return r


class JsonResponse(Response):
    def __init__(self, response) -> None:
        super().__init__(response.status_code, dict(response.headers), response.json(), response.request.url)


class MultipartResponse(Response):
    def __init__(self, response) -> None:
        parts: List[Dict] = list()
        for part in decoder.MultipartDecoder.from_response(response).parts:
            parts.append(json.loads(part.text))
        super().__init__(response.status_code, dict(response.headers), parts, response.request.url)
