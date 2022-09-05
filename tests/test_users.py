import pytest
import random
import string
from app import schemas
from app.config import settings
from jose import jwt


def test_root(client):  # client
    resp = client.get("/")
    assert resp.json().get('message') == 'My api of course'
    assert resp.status_code == 200


def test_create_user(client):  # client
    email = f"test_{random.choice(string.ascii_letters)}{str(random.randint(1, 1000000))}@mail.com"
    resp = client.post(
        '/users/', json={"email": email, "password": "wordpass"})
    new_user = schemas.UserResponse(**resp.json())
    new_user.email == email
    assert resp.status_code == 201


def test_login_user(client, test_user):  # client
    resp = client.post(
        '/login', data={"username": test_user['email'], "password": test_user['password']})
    assert resp.status_code == 200
    login = schemas.Token(**resp.json())
    payload = jwt.decode(login.token, settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login.token_type == 'bearer'


def test_incorrect_user(client, test_user):
    email = f"test_{random.choice(string.ascii_letters)}{str(random.randint(1, 1000000))}@mail.com"
    resp = client.post(
        '/login', data={"username": email, "password": test_user['password']})

    assert resp.status_code == 403
    assert resp.json()['detail'] == 'Invalid Credentials'


def test_incorrect_password(client, test_user):
    password = f"{random.choice(string.ascii_letters)*3}pass{random.choice(string.ascii_letters)}{str(random.randint(1, 1000))}"
    resp = client.post(
        '/login', data={"username": test_user['email'], "password": password})

    assert resp.status_code == 403
    assert resp.json()['detail'] == 'Invalid Credentials'


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@nuevo.com', 'password123', 403),
    ('adbgeorge@gmail.com', 'wrongpassword', 403),
    ('test_R47399@mail.com', 'wordpass', 403),
    (None, 'password123', 422),
    ('test_r42525@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
