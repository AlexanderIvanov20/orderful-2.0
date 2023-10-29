from pydantic import BaseModel, ConfigDict, EmailStr


class BaseUser(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    active: bool = False
    superuser: bool = False


class CreateUser(BaseUser):
    name: str
    email: EmailStr
    password: str
    active: bool


class UpdateUser(BaseUser):
    password: str | None = None


class User(BaseUser):
    id: int

    model_config = ConfigDict(from_attributes=True)
