from typing import Callable

import pytest
from fastapi.testclient import TestClient
from jsonschema import validate
from sqlalchemy.orm import Session

from orderful.models.products import Product
from orderful.models.users import User
from tests.factories import CategoryFactory, CategoryProductAssociationFactory, ProductFactory, UserFactory
from tests.routers import constants


def test_get_products_view_schema(
    authenticated_client: Callable[[User], TestClient],
    active_user: User,
    product_factory: ProductFactory,
):
    product_factory(user=active_user)

    client = authenticated_client(active_user)

    response = client.get(constants.PRODUCTS_URL)
    assert response.status_code == 200

    response = response.json()
    validate(instance=response[0], schema=constants.PRODUCTS_SCHEMA)


@pytest.mark.parametrize(
    "offset, limit, expected_id, expected_length",
    (
        (1, 10, 2, 10),
        (5, 10, 6, 10),
        (-5, 10, 1, 10),
        (-5, -10, 1, 20),
    ),
)
def test_get_products_view_pagination(
    authenticated_client: Callable[[User], TestClient],
    active_user: User,
    expected_id: int,
    expected_length: int,
    product_factory: ProductFactory,
    limit: int,
    offset: int,
):
    for _ in range(20):
        product_factory(user=active_user)

    client = authenticated_client(active_user)

    response = client.get(f"{constants.PRODUCTS_URL}?offset={offset}&limit={limit}")
    assert response.status_code == 200

    response = response.json()

    assert len(response) == expected_length
    assert response[0]["id"] == expected_id


def test_get_products_view_superuser(
    authenticated_client: Callable[[User], TestClient],
    superuser: User,
    product_factory: ProductFactory,
    user_factory: UserFactory,
):
    for _ in range(5):
        product_factory(user=user_factory())

    client = authenticated_client(superuser)

    response = client.get(constants.PRODUCTS_URL)
    assert response.status_code == 200

    response = response.json()

    assert len(response) == 5


def test_create_product_view(
    authenticated_client: Callable[[User], TestClient],
    active_user: User,
    session: Session,
    category_factory: CategoryFactory,
):
    category_1 = category_factory()
    category_2 = category_factory(parent=category_1)

    data = {
        "name": "Test Product",
        "article": "sdfa@lassdk!",
        "price": 200,
        "quantity": 20,
        "categories": [
            category_1.id,
            category_2.id,
        ],
    }

    client = authenticated_client(active_user)

    response = client.post(constants.PRODUCTS_URL, json=data)
    assert response.status_code == 201, response.json()

    assert session.query(Product).count() == 1


def test_update_product_view(
    authenticated_client: Callable[[User], TestClient],
    active_user: User,
    session: Session,
    product_factory: ProductFactory,
    category_factory: CategoryFactory,
    category_product_association_factory: CategoryProductAssociationFactory,
):
    category_1 = category_factory()
    category_2 = category_factory(parent=category_1)
    category_3 = category_factory()

    product = product_factory(user=active_user)

    category_product_association_factory(category=category_1, product=product)

    data = {
        "name": "Test Product",
        "article": "sdfa@lassdk!",
        "price": 200,
        "quantity": 20,
        "categories": [
            category_2.id,
            category_3.id,
        ],
    }

    client = authenticated_client(active_user)

    response = client.put(f"{constants.PRODUCTS_URL}/{product.id}", json=data)
    assert response.status_code == 200

    session.refresh(product)
    response = response.json()

    assert response["id"] == product.id
    assert response["name"] == product.name
    assert response["price"] == str(product.price)
    assert response["categories"][0]["category_id"] == category_2.id
    assert response["categories"][1]["category_id"] == category_3.id


def test_get_product_view(
    authenticated_client: Callable[[User], TestClient],
    active_user: User,
    product_factory: ProductFactory,
):
    product = product_factory(user=active_user)

    client = authenticated_client(active_user)

    response = client.get(f"{constants.PRODUCTS_URL}/{product.id}")
    assert response.status_code == 200

    response = response.json()
    validate(instance=response, schema=constants.PRODUCTS_SCHEMA)

    assert response["id"] == product.id


def test_get_product_view_product_does_not_exist(
    authenticated_client: Callable[[User], TestClient],
    active_user: User,
):
    client = authenticated_client(active_user)

    response = client.get(f"{constants.PRODUCTS_URL}/99999")
    assert response.status_code == 404


def test_delete_product_view(
    authenticated_client: Callable[[User], TestClient],
    active_user: User,
    product_factory: ProductFactory,
):
    product = product_factory(user=active_user)

    client = authenticated_client(active_user)

    response = client.delete(f"{constants.PRODUCTS_URL}/{product.id}")
    assert response.status_code == 204
