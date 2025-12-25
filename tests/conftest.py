import pytest
import allure

from helpers.courier import create_courier, delete_courier, generate_courier_payload, get_courier_id


@pytest.fixture
def courier_payload():
    return generate_courier_payload()


@pytest.fixture
def courier_deleter():
    """
    Регистрируем courier_id на удаление в teardown (вместо try/finally в тестах).
    """
    ids: list[int] = []

    def _register(courier_id: int | None):
        if courier_id is not None:
            ids.append(courier_id)

    yield _register

    for courier_id in ids:
        with allure.step(f"Удаляем курьера id={courier_id} (teardown)"):
            delete_courier(courier_id)


@pytest.fixture
def created_courier(courier_payload, courier_deleter):
    """
    Создаёт курьера ДО теста, удаляет ПОСЛЕ теста.
    Возвращает (courier_id, payload).
    """
    with allure.step("Подготовка: создаём курьера"):
        response = create_courier(courier_payload)
        assert response.status_code == 201, (
            f"Не удалось создать курьера. Код: {response.status_code}, тело: {response.text}"
        )

    with allure.step("Подготовка: получаем courier_id после создания"):
        courier_id = get_courier_id({"login": courier_payload["login"], "password": courier_payload["password"]})
        assert courier_id is not None, "Не удалось получить courier_id после создания"

    courier_deleter(courier_id)
    return courier_id, courier_payload
