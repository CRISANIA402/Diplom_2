import allure
import pytest
import requests

from urls import CREATE_USER


@allure.title("Создание уникального пользователя")
def test_create_unique_user(user_data):
    with allure.step("Отправляем запрос на регистрацию"):
        response = requests.post(CREATE_USER, json=user_data)

    with allure.step("Проверяем ответ: 200 и success=True"):
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["email"] == user_data["email"]


@allure.title("Создание уже зарегистрированного пользователя")
def test_create_existing_user(registered_user):
    with allure.step("Пробуем зарегистрироваться повторно с тем же email"):
        response = requests.post(CREATE_USER, json=registered_user)

    with allure.step("Проверяем ответ: 403 и сообщение об ошибке"):
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"


@allure.title("Создание пользователя без одного из обязательных полей")
@pytest.mark.parametrize("missing_field", ["email", "password", "name"])
def test_create_user_missing_field(user_data, missing_field):
    payload = user_data.copy()
    del payload[missing_field]

    with allure.step(f"Отправляем запрос без поля {missing_field}"):
        response = requests.post(CREATE_USER, json=payload)

    with allure.step("Проверяем ответ: 403 и сообщение о пустых полях"):
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"
