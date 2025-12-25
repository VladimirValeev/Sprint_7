import allure

from helpers.orders import get_orders_list


@allure.suite("Orders")
@allure.feature("Orders list")
class TestOrdersList:

    @allure.title("Список заказов: возвращает 200 и массив orders")
    def test_get_orders_list_returns_orders(self):
        response = get_orders_list()

        assert response.status_code == 200
        body = response.json()

        assert "orders" in body
        assert isinstance(body["orders"], list)
