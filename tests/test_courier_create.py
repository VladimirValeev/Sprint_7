import pytest
import allure

from data.expected import COURIER_CREATED_OK, MSG_LOGIN_ALREADY_USED, MSG_NOT_ENOUGH_DATA_CREATE
from helpers.courier import create_courier, get_courier_id


@allure.suite("Courier")
@allure.feature("Create courier")
class TestCourierCreate:

    @allure.title("Создание курьера: успешный запрос возвращает 201 и ok=true")
    def test_create_courier_success_returns_201_and_ok_true(self, courier_payload, courier_deleter):
        response = create_courier(courier_payload)

        assert response.status_code == 201
        assert response.json() == COURIER_CREATED_OK

        courier_id = get_courier_id({"login": courier_payload["login"], "password": courier_payload["password"]})
        courier_deleter(courier_id)

    @allure.title("Создание курьера: повторное создание с тем же логином возвращает 409")
    def test_create_two_same_couriers_returns_409(self, courier_payload, courier_deleter):
        response_1 = create_courier(courier_payload)
        assert response_1.status_code == 201
        assert response_1.json() == COURIER_CREATED_OK

        response_2 = create_courier(courier_payload)
        assert response_2.status_code == 409
        assert response_2.json()["message"] == MSG_LOGIN_ALREADY_USED

        courier_id = get_courier_id({"login": courier_payload["login"], "password": courier_payload["password"]})
        courier_deleter(courier_id)

    @allure.title("Создание курьера: без обязательного поля возвращает 400")
    @pytest.mark.parametrize("broken_field", ["login", "password"])
    def test_create_courier_without_required_field_returns_400(self, courier_payload, broken_field):
        courier_payload.pop(broken_field)

        response = create_courier(courier_payload)

        assert response.status_code == 400
        assert response.json()["message"] == MSG_NOT_ENOUGH_DATA_CREATE
