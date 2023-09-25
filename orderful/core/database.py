from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orderful.core.settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, autoflush=False, expire_on_commit=False)
