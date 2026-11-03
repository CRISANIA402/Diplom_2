import random
import string


def generate_email():
    return f"test_{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com"


def generate_password():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def generate_name():
    return "".join(random.choices(string.ascii_lowercase, k=6))
