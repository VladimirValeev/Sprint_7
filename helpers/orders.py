import requests

from helpers.urls import CREATE_ORDER_URL, ORDERS_LIST_URL


def generate_order_payload(colors=None) -> dict:
    payload = {
        "firstName": "Test",
        "lastName": "User",
        "address": "Москва, Красная площадь, 1",
        "metroStation": 4,
        "phone": "+79999999999",
        "rentTime": 3,
        "deliveryDate": "2025-12-31",
        "comment": "Тестовый заказ",
    }

    # если colors передан:
    # - [] → отправится пустой список
    # - ["BLACK"] / ["GREY"] / ["BLACK", "GREY"]
    # если colors == None → поле color не добавляем вообще
    if colors is not None:
        payload["color"] = colors

    return payload


def create_order(payload: dict) -> requests.Response:
    return requests.post(CREATE_ORDER_URL, json=payload, timeout=30)


def get_orders_list() -> requests.Response:
    return requests.get(ORDERS_LIST_URL, timeout=30)
