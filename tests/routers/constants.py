from orderful.core.settings import settings
from tests.utils import strict_object

REGISTER_URL = f"{settings.REST_ROUTE}/auth/register"
LOGIN_URL = f"{settings.REST_ROUTE}/auth/login"
ME_URL = f"{settings.REST_ROUTE}/auth/me"

REGISTER_SCHEMA = strict_object(
    {
        "id": {"type": ["integer"]},
        "name": {"type": ["string"]},
        "email": {"type": ["string"]},
        "superuser": {"type": ["boolean"]},
        "active": {"type": ["boolean"]},
    }
)
LOGIN_SCHEMA = strict_object(
    {
        "access_token": {"type": ["string"]},
        "token_type": {"type": ["string"]},
    }
)
ME_SCHEMA = REGISTER_SCHEMA

USERS_URL = f"{settings.REST_ROUTE}/users"

USERS_SCHEMA = REGISTER_SCHEMA
