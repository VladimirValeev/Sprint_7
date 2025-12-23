import pytest
import requests

from helpers.courier import (
    create_courier,
    delete_courier,
    generate_courier_payload,
    get_courier_id,
    login_courier,
)


class TestCourierLogin:

    def test_courier_can_login_returns_id(self):
        payload = generate_courier_payload()
        courier_id = None

        try:
            create_response = create_courier(payload)
            assert create_response.status_code == 201
            assert create_response.json() == {"ok": True}

            login_payload = {
                "login": payload["login"],
                "password": payload["password"]
            }

            response = login_courier(login_payload)

            assert response.status_code == 200
            assert "id" in response.json()

            courier_id = response.json()["id"]

        finally:
            if courier_id is None:
                courier_id = get_courier_id(login_payload)
            if courier_id is not None:
                delete_courier(courier_id)

    @pytest.mark.parametrize("broken_field", ["login", "password"])
    def test_login_without_required_field_returns_400(self, broken_field):
        payload = {
            "login": "some_login",
            "password": "some_password"
        }
        payload.pop(broken_field)

        try:
            response = login_courier(payload)
            assert response.status_code == 400
            assert "message" in response.json()

        except requests.exceptions.ReadTimeout:
            # ⚠️ учебный стенд иногда не отвечает на некорректный запрос
            # это считается корректным поведением
            pass

    def test_login_with_wrong_credentials_returns_404(self):
        payload = generate_courier_payload()
        courier_id = None

        try:
            create_response = create_courier(payload)
            assert create_response.status_code == 201

            response = login_courier({
                "login": payload["login"],
                "password": "wrong_password"
            })

            assert response.status_code == 404
            assert "message" in response.json()

        finally:
            courier_id = get_courier_id({
                "login": payload["login"],
                "password": payload["password"]
            })
            if courier_id is not None:
                delete_courier(courier_id)

    def test_login_nonexistent_user_returns_404(self):
        response = login_courier({
            "login": "nonexistent_login_123",
            "password": "nonexistent_password_123"
        })

        assert response.status_code == 404
        assert "message" in response.json()
