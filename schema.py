import abc
import re
from typing import Optional, Type

import pydantic

PASSWORD_LOWERCASE = re.compile(r"[a-z]")
PASSWORD_UPPERCASE = re.compile(r"[A-Z]")
PASSWORD_DIGITS = re.compile(r"[0-9]")
PASSWORD_MIN_LENGTHS = 8
PASSWORD_MAX_LENGTH = 32


class AbstractUser(pydantic.BaseModel, abc.ABC):
    name: str
    email: str
    password: str


class Login(AbstractUser):
    name: str
    email: Optional[str] = None
    password: str 


class CreateUser(AbstractUser):

    @pydantic.field_validator("password")
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < PASSWORD_MIN_LENGTHS:
            raise ValueError(f"Minimal length of password is {PASSWORD_MIN_LENGTHS}")
        if len(v) > PASSWORD_MAX_LENGTH:
            raise ValueError(f"Maxima length of password is {PASSWORD_MAX_LENGTH}")
        if not PASSWORD_LOWERCASE.search(v):
            raise ValueError("Password must contain lowercase characters")
        if not PASSWORD_UPPERCASE.search(v):
            raise ValueError("Password must contain uppercase characters")
        return v


class PatchUser(CreateUser):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UpdateUser(CreateUser):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class CreateArticle(pydantic.BaseModel):
    title: str
    description: str


class UpdateArticle(pydantic.BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


SCHEMA_MODEL = Type[Login | CreateUser | UpdateUser | CreateArticle | UpdateArticle]