# helpers/http.py

import allure
import requests

DEFAULT_TIMEOUT = 15


def post(url: str, payload: dict | None = None, step_name: str = "POST request"):
    with allure.step(f"{step_name}: POST {url}"):
        return requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT)


def get(url: str, params: dict | None = None, step_name: str = "GET request"):
    with allure.step(f"{step_name}: GET {url}"):
        return requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)


def delete(url: str, step_name: str = "DELETE request"):
    with allure.step(f"{step_name}: DELETE {url}"):
        return requests.delete(url, timeout=DEFAULT_TIMEOUT)
