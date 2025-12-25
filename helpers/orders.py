# helpers/orders.py

import random

from helpers.http import get, post
from helpers.urls import CREATE_ORDER_URL, GET_ORDERS_LIST_URL


def generate_order_payload(colors):
    # минимально достаточный корректный payload под учебный API
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2025-12-31",
        "comment": f"Test order {random.randint(1, 10_000)}",
    }

    # цвет может быть None (поле не передаём)
    if colors is not None:
        payload["color"] = colors

    return payload


def create_order(payload: dict):
    return post(CREATE_ORDER_URL, payload, step_name="Создать заказ")


def get_orders_list():
    return get(GET_ORDERS_LIST_URL, step_name="Получить список заказов")
