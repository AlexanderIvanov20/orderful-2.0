from typing import Callable

from fastapi.testclient import TestClient
from jsonschema import validate

from orderful.models.users import User
from tests.constants import TEST_PASSWORD
from tests.factories import UserFactory
from tests.routers import constants


def test_register_view(client: TestClient):
    data = {
        "name": "Test User",
        "email": "test_user@orderful.com",
        "password": "1a;skdfj1p4",
        "superuser": False,
        "active": False,
    }

    response = client.post(constants.REGISTER_URL, json=data)
    assert response.status_code == 201

    response = response.json()
    validate(instance=response, schema=constants.REGISTER_SCHEMA)


def test_login_view(client: TestClient, user_factory: UserFactory):
    user = user_factory()

    data = {
        "username": user.email,
        "password": TEST_PASSWORD,
    }

    response = client.post(constants.LOGIN_URL, data=data)
    assert response.status_code == 200

    response = response.json()
    validate(instance=response, schema=constants.LOGIN_SCHEMA)


def test_me_view(authenticated_client: Callable[[User], TestClient], user_factory: UserFactory):
    user = user_factory(active=True)

    client = authenticated_client(user)

    response = client.get(constants.ME_URL)
    assert response.status_code == 200

    response = response.json()
    validate(instance=response, schema=constants.ME_SCHEMA)


def test_me_view_user_not_active(
    authenticated_client: Callable[[User], TestClient], user_factory: UserFactory
):
    user = user_factory(active=False)

    client = authenticated_client(user)

    response = client.get(constants.ME_URL)
    assert response.status_code == 400

    response = response.json()
    assert response["detail"] == "The current user is inactive."
