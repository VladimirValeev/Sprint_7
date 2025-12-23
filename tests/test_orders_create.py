import pytest

from helpers.orders import create_order, generate_order_payload


class TestOrderCreate:
    @pytest.mark.parametrize(
        "colors",
        [
            ["BLACK"],          # один цвет
            ["GREY"],           # один цвет
            ["BLACK", "GREY"],  # оба цвета
            [],                 # пустой список
            None,               # поле color не передаём
        ],
    )
    def test_create_order_returns_track(self, colors):
        payload = generate_order_payload(colors)

        response = create_order(payload)

        assert response.status_code == 201
        body = response.json()
        assert "track" in body
        assert body["track"] is not None
