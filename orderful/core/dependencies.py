from typing import Generator

from orderful.core.database import SessionLocal


def get_session() -> Generator:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
