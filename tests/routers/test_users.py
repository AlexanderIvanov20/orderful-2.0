from typing import Callable

import pytest
from fastapi.testclient import TestClient
from jsonschema import validate

from orderful.models.users import User
from tests.factories import UserFactory
from tests.routers import constants


def test_get_users_view_schema(
    authenticated_client: Callable[[User], TestClient], superuser: User, user_factory: UserFactory
) -> None:
    for _ in range(3):
        user_factory(active=True)

    client = authenticated_client(superuser)

    response = client.get(constants.USERS_URL)
    assert response.status_code == 200, response.json()

    response = response.json()
    validate(instance=response[0], schema=constants.USERS_SCHEMA)


@pytest.mark.parametrize(
    "offset, limit, expected_id, expected_length",
    (
        (1, 10, 2, 10),
        (5, 10, 6, 10),
        (-5, 10, 1, 10),
        (-5, -10, 1, 21),
    ),
)
def test_get_users_view_pagination(
    authenticated_client: Callable[[User], TestClient],
    superuser: User,
    expected_id: int,
    expected_length: int,
    limit: int,
    offset: int,
    user_factory: UserFactory,
):
    for _ in range(20):
        user_factory()

    client = authenticated_client(superuser)

    response = client.get(f"{constants.USERS_URL}?offset={offset}&limit={limit}")
    assert response.status_code == 200

    response = response.json()

    assert len(response) == expected_length
    assert response[0]["id"] == expected_id


def test_update_user_view(authenticated_client: Callable[[User], TestClient], active_user: User):
    data = {
        "name": "Test User",
    }

    client = authenticated_client(active_user)

    response = client.put(f"{constants.USERS_URL}/{active_user.id}", json=data)
    assert response.status_code == 200

    response = response.json()

    assert response["id"] == active_user.id
    assert response["name"] == data["name"]


def test_update_user_view_password(authenticated_client: Callable[[User], TestClient], active_user: User):
    data = {
        "password": "some_new_password",
    }

    client = authenticated_client(active_user)

    response = client.put(f"{constants.USERS_URL}/{active_user.id}", json=data)
    assert response.status_code == 200

    data["username"] = active_user.email

    response = client.post(constants.LOGIN_URL, data=data)
    assert response.status_code == 200


def test_get_user_view(
    authenticated_client: Callable[[User], TestClient], active_user: User, user_factory: UserFactory
):
    client = authenticated_client(active_user)

    response = client.get(f"{constants.USERS_URL}/{active_user.id}")
    assert response.status_code == 200

    response = response.json()
    validate(instance=response, schema=constants.USERS_SCHEMA)

    assert response["id"] == active_user.id


def test_delete_user_view(
    authenticated_client: Callable[[User], TestClient], superuser: User, user_factory: UserFactory
):
    user = user_factory()

    client = authenticated_client(superuser)

    response = client.delete(f"{constants.USERS_URL}/{user.id}")
    assert response.status_code == 204
