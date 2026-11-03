import allure
import pytest
import requests

from helpers import generate_email, generate_name, generate_password
from urls import BASE_URL, CREATE_USER, DELETE_USER, LOGIN_USER


@pytest.fixture
def user_data():
    """Данные нового пользователя, уникальные для каждого теста"""
    return {
        "email": generate_email(),
        "password": generate_password(),
        "name": generate_name(),
    }


@pytest.fixture
def registered_user(user_data):
    """Создаёт пользователя, возвращает его данные с токеном
    и удаляет пользователя после теста"""
    response = requests.post(CREATE_USER, json=user_data)
    token = response.json().get("accessToken")

    user_data["token"] = token

    yield user_data

    if token:
        with allure.step("Удаляем тестового пользователя"):
            requests.delete(DELETE_USER, headers={"Authorization": token})


@pytest.fixture
def access_token(registered_user):
    """Токен авторизации зарегистрированного пользователя"""
    payload = {
        "email": registered_user["email"],
        "password": registered_user["password"],
    }
    response = requests.post(LOGIN_USER, json=payload)
    return response.json().get("accessToken")


@pytest.fixture
def available_ingredients():
    """Два реальных _id ингредиентов из справочника"""
    response = requests.get(f"{BASE_URL}/api/ingredients")
    ingredients = response.json().get("data", [])
    return [ing["_id"] for ing in ingredients[:2]]
