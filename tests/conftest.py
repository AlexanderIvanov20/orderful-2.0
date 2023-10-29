from typing import Callable, Generator

import pytest
from fastapi.testclient import TestClient
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy import Connection, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from orderful.core.dependencies import get_session
from orderful.core.settings import settings
from orderful.main import app
from orderful.models.base import Base
from orderful.models.users import User
from orderful.services.users import UserService
from tests.constants import TEST_PASSWORD
from tests.factories import UserFactory

pg = create_postgres_fixture()


@pytest.fixture
def alembic_engine(pg):
    return pg


@pytest.fixture(scope="session")
def connection():
    engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URI, connect_args={"check_same_thread": False})
    return engine.connect()


@pytest.fixture
def setup_database(connection: Connection) -> Generator:
    Base.metadata.create_all(bind=connection)

    yield

    Base.metadata.drop_all(bind=connection)


@pytest.fixture
def session(connection: Connection, setup_database: Generator) -> Generator:
    yield scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=connection))


@pytest.fixture(autouse=True)
def setup_application(session: Session) -> Generator:
    app.dependency_overrides[get_session] = lambda: session

    UserFactory._meta.sqlalchemy_session = session

    yield


@pytest.fixture
def user_factory(session: Session) -> UserFactory:
    return UserFactory


@pytest.fixture
def active_user(user_factory: UserFactory) -> User:
    return user_factory(active=True)


@pytest.fixture
def superuser(active_user: User) -> User:
    active_user.superuser = True
    return active_user


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def authenticated_client(client: TestClient, session: Session) -> Callable[[User], TestClient]:
    def _authenticated_client(user: User) -> TestClient:
        token = UserService(session).authenticate(user.email, TEST_PASSWORD)

        client.headers["Authorization"] = f"Bearer {token.access_token}"
        return client

    return _authenticated_client
