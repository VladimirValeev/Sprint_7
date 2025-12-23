import pytest

from helpers.courier import (
    create_courier,
    create_and_get_courier_id,
    delete_courier,
    generate_courier_payload,
)


class TestCourierCreate:
    def test_create_courier_success_returns_201_and_ok_true(self):
        payload = generate_courier_payload()
        courier_id = None

        try:
            response = create_courier(payload)

            assert response.status_code == 201
            assert response.json() == {"ok": True}

            courier_id = create_and_get_courier_id(payload)
        finally:
            if courier_id is not None:
                delete_courier(courier_id)

    def test_create_two_same_couriers_returns_409(self):
        payload = generate_courier_payload()
        courier_id = None

        try:
            response_1 = create_courier(payload)
            assert response_1.status_code == 201
            assert response_1.json() == {"ok": True}

            response_2 = create_courier(payload)
            assert response_2.status_code == 409
            assert response_2.json()["message"] == "Этот логин уже используется. Попробуйте другой."

            courier_id = create_and_get_courier_id(payload)
        finally:
            if courier_id is not None:
                delete_courier(courier_id)

    @pytest.mark.parametrize("broken_field", ["login", "password"])
    def test_create_courier_without_required_field_returns_400(self, broken_field):
        payload = generate_courier_payload()
        payload.pop(broken_field)

        response = create_courier(payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
