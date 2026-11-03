import allure
import requests

from urls import LOGIN_USER


@allure.title("Вход под существующим пользователем")
def test_login_success(registered_user):
    payload = {
        "email": registered_user["email"],
        "password": registered_user["password"],
    }

    with allure.step("Отправляем запрос на логин"):
        response = requests.post(LOGIN_USER, json=payload)

    with allure.step("Проверяем ответ: 200, success=True и токены на месте"):
        body = response.json()
        assert response.status_code == 200
        assert body["success"] is True
        assert "accessToken" in body and "refreshToken" in body


@allure.title("Вход с неверным логином и паролем")
def test_login_wrong_credentials(user_data):
    payload = {
        "email": "wrong_user@example.com",
        "password": "wrong_password_123",
    }

    with allure.step("Отправляем запрос с неверными данными"):
        response = requests.post(LOGIN_USER, json=payload)

    with allure.step("Проверяем ответ: 401 и сообщение об ошибке"):
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"
