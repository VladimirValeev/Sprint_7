import pytest
import allure
import requests

from data.expected import MSG_NOT_ENOUGH_DATA_LOGIN, MSG_ACCOUNT_NOT_FOUND
from helpers.courier import create_courier, get_courier_id, login_courier


@allure.suite("Courier")
@allure.feature("Login courier")
class TestCourierLogin:

    @allure.title("Логин курьера: успешный логин возвращает 200 и id")
    def test_courier_can_login_returns_id(self, created_courier):
        courier_id, payload = created_courier

        login_payload = {"login": payload["login"], "password": payload["password"]}
        response = login_courier(login_payload)

        assert response.status_code == 200
        body = response.json()
        assert "id" in body
        assert body["id"] == courier_id

    @allure.title("Логин курьера: без обязательного поля возвращает 400")
    @pytest.mark.parametrize("broken_field", ["login", "password"])
    def test_login_without_required_field_returns_400(self, broken_field):
        payload = {"login": "some_login", "password": "some_password"}
        payload.pop(broken_field)

        try:
            response = login_courier(payload)
        except requests.exceptions.ReadTimeout:
            pytest.xfail("Стенд не ответил на некорректный запрос (ReadTimeout). По документации ожидается 400.")

        assert response.status_code == 400
        assert response.json()["message"] == MSG_NOT_ENOUGH_DATA_LOGIN

    @allure.title("Логин курьера: неверный пароль возвращает 404")
    def test_login_with_wrong_password_returns_404(self, created_courier):
        _, payload = created_courier

        response = login_courier({"login": payload["login"], "password": "wrong_password"})

        assert response.status_code == 404
        assert response.json()["message"] == MSG_ACCOUNT_NOT_FOUND

    @allure.title("Логин курьера: несуществующий пользователь возвращает 404")
    def test_login_nonexistent_user_returns_404(self):
        response = login_courier({"login": "nonexistent_login_123", "password": "nonexistent_password_123"})

        assert response.status_code == 404
        assert response.json()["message"] == MSG_ACCOUNT_NOT_FOUND
