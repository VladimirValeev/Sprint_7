# tests/test_orders_create.py

import allure
import pytest

from helpers.orders import create_order, generate_order_payload


@allure.suite("Orders")
@allure.feature("Create order")
class TestOrderCreate:

    @allure.title("Можно создать заказ с разными значениями color — возвращается 201 и track")
    @pytest.mark.parametrize(
        "colors",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            [],
            None,
        ],
    )
    def test_create_order_returns_track(self, colors):
        payload = generate_order_payload(colors)

        response = create_order(payload)

        assert response.status_code == 201
        body = response.json()
        assert "track" in body
        assert body["track"] is not None
