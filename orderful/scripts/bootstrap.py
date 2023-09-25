import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

from orderful.core.database import SessionLocal
from orderful.core.settings import settings
from orderful.schemas.users import CreateUser
from orderful.services.users import UserService

logger = logging.getLogger(__name__)


def validate_database_connection() -> Session:
    try:
        session = SessionLocal()

        session.execute(text("SELECT 1"))
    except Exception as exc:
        logger.error(f"[-] {exc}")
        raise exc

    return session


def create_user(session: Session, email: str, password: str = None, **kwargs) -> None:
    user_service = UserService(session)

    user = user_service.filter_by(email=email).one_or_none()

    if not user:
        name = email.rsplit("@")[0]
        data = CreateUser(
            name=name,
            email=email,
            password=password or name,
            active=True,
            **kwargs,
        )
        new_user = user_service.create(data)

        logger.info(f"\t[+] Created user: {new_user}.")


def run() -> None:
    session = validate_database_connection()

    logger.info("[+] Bootstrapping a newly created database...")

    create_user(
        session,
        email=settings.SUPERUSER_EMAIL,
        password=settings.SUPERUSER_PASSWORD,
        superuser=True,
    )
    create_user(session, email="info@orderful.com")


if __name__ == "__main__":
    run()
