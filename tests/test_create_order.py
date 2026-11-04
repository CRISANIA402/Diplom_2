import allure
import pytest
import requests

from urls import ORDERS


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth(self, access_token, available_ingredients):
        headers = {"Authorization": access_token}
        payload = {"ingredients": available_ingredients}

        with allure.step("Отправляем заказ от авторизованного пользователя"):
            response = requests.post(ORDERS, headers=headers, json=payload)

        with allure.step("Проверяем ответ: 200, success=True, номер заказа есть"):
            body = response.json()
            assert response.status_code == 200
            assert body["success"] is True
            assert body["order"]["number"] > 0

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, available_ingredients):
        payload = {"ingredients": available_ingredients}

        with allure.step("Отправляем заказ без токена"):
            response = requests.post(ORDERS, json=payload)

        with allure.step("API позволяет создать заказ без авторизации: 200 и success=True"):
            body = response.json()
            assert response.status_code == 200
            assert body["success"] is True
            assert body["order"]["number"] > 0

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, access_token):
        headers = {"Authorization": access_token}
        payload = {"ingredients": []}

        with allure.step("Отправляем заказ с пустым списком ингредиентов"):
            response = requests.post(ORDERS, headers=headers, json=payload)

        with allure.step("Проверяем ответ: 400 и сообщение о пустых ингредиентах"):
            assert response.status_code == 400
            assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_ingredient_hash(self, access_token):
        headers = {"Authorization": access_token}
        payload = {"ingredients": ["invalid_hash_12345"]}

        with allure.step("Отправляем заказ с несуществующим хешем"):
            response = requests.post(ORDERS, headers=headers, json=payload)

        with allure.step("Проверяем ответ: 500 — сервер не справился с неверным хешем"):
            assert response.status_code == 500
