from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from orderful.core.settings import settings
from orderful.schemas.tokens import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.REST_ROUTE}/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordServiceMixin:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class TokenServiceMixin:
    @staticmethod
    def create_access_token(subject: str | None) -> str:
        return jwt.encode(
            {
                "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                "sub": str(subject),
            },
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )

    @staticmethod
    def get_token_data(token: str, secret_key: str, authenticate_value: str = None) -> TokenPayload:
        try:
            payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
            token_data = TokenPayload(**payload)
        except (JWTError, ValidationError) as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate the credentials.",
                headers={"WWW-Authenticate": authenticate_value} if authenticate_value else None,
            ) from exc

        return token_data
