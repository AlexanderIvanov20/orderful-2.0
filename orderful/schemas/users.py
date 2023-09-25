from pydantic import BaseModel, ConfigDict, EmailStr


class BaseUser(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    active: bool = False
    superuser: bool = False


class CreateUser(BaseUser):
    name: str
    email: EmailStr
    password: str


class UpdateUser(BaseUser):
    pass


class User(BaseUser):
    id: int

    model_config = ConfigDict(from_attributes=True)
