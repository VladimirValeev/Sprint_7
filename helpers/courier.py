import random
import string

from helpers.http import delete, post
from helpers.urls import CREATE_COURIER_URL, DELETE_COURIER_URL, LOGIN_COURIER_URL


def _random_str(n: int = 10) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(n))


def generate_courier_payload() -> dict:
    login = f"courier_{_random_str(10)}"
    password = _random_str(12)
    first_name = f"name_{_random_str(6)}"
    return {"login": login, "password": password, "firstName": first_name}


def create_courier(payload: dict):
    # allure.step должен быть внутри helpers.http.post (у тебя уже есть step_name)
    return post(CREATE_COURIER_URL, payload, step_name="Создать курьера")


def login_courier(payload: dict):
    return post(LOGIN_COURIER_URL, payload, step_name="Логин курьера")


def delete_courier(courier_id: int):
    return delete(f"{DELETE_COURIER_URL}/{courier_id}", step_name="Удалить курьера")


def get_courier_id(payload: dict) -> int | None:
    """
    Получаем id через логин.
    Если логин неуспешен — вернём None.
    """
    resp = login_courier(payload)
    if resp.status_code != 200:
        return None
    body = resp.json()
    return body.get("id")
