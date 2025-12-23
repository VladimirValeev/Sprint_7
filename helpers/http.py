import requests
from requests.exceptions import ReadTimeout, ConnectionError


DEFAULT_TIMEOUT = 30


def post(url: str, data: dict | None = None, timeout: int = DEFAULT_TIMEOUT, retries: int = 1) -> requests.Response:
    last_exc = None
    for _ in range(retries + 1):
        try:
            return requests.post(url, data=data, timeout=timeout)
        except (ReadTimeout, ConnectionError) as exc:
            last_exc = exc
    raise last_exc


def delete(url: str, timeout: int = DEFAULT_TIMEOUT, retries: int = 1) -> requests.Response:
    last_exc = None
    for _ in range(retries + 1):
        try:
            return requests.delete(url, timeout=timeout)
        except (ReadTimeout, ConnectionError) as exc:
            last_exc = exc
    raise last_exc
