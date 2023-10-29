from orderful.core.settings import settings
from tests.utils import strict_object

REGISTER_URL = f"{settings.REST_ROUTE}/auth/register"
LOGIN_URL = f"{settings.REST_ROUTE}/auth/login"
ME_URL = f"{settings.REST_ROUTE}/auth/me"
USERS_URL = f"{settings.REST_ROUTE}/users"
PRODUCTS_URL = f"{settings.REST_ROUTE}/products"

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
USERS_SCHEMA = REGISTER_SCHEMA
PRODUCTS_SCHEMA = strict_object(
    {
        "id": {"type": ["integer"]},
        "name": {"type": ["string"]},
        "price": {"type": ["string"]},
        "article": {"type": ["string"]},
        "quantity": {"type": ["integer"]},
        "user_id": {"type": ["integer"]},
        "categories": {
            "type": "array",
            "items": strict_object(
                {
                    "category_id": {"type": ["integer"]},
                }
            ),
        },
    }
)
