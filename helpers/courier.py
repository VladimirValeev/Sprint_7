import random
import string

from helpers.http import post, delete
from helpers.urls import CREATE_COURIER_URL, LOGIN_COURIER_URL, DELETE_COURIER_URL


def _random_string(length: int = 10) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_courier_payload() -> dict:
    return {
        "login": _random_string(10),
        "password": _random_string(10),
        "firstName": _random_string(10),
    }


def create_courier(payload: dict):
    return post(CREATE_COURIER_URL, data=payload)


def login_courier(payload: dict):
    return post(LOGIN_COURIER_URL, data=payload)


def get_courier_id(payload: dict) -> int | None:
    response = login_courier(payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None


def create_and_get_courier_id(payload: dict) -> int | None:
    create_courier(payload)  # даже если 409 — ок
    return get_courier_id({"login": payload.get("login"), "password": payload.get("password")})


def delete_courier(courier_id: int):
    return delete(f"{DELETE_COURIER_URL}/{courier_id}")
