import pytest
from pytest_mock_resources import create_postgres_fixture


pg = create_postgres_fixture()


@pytest.fixture
def alembic_engine(pg):
    return pg
