import datetime
import os
import atexit
import uuid
from typing import List, Type

from sqlalchemy import DateTime, String, create_engine, func, UUID, Boolean, Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'secret')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'app')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'app')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(101), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    tokens: Mapped[List["Token"]] = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    articles: Mapped[List["Article"]] = relationship("Article", back_populates="user", cascade="all, delete-orphan")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "articles": [a.dict for a in self.articles],
        }


class Token(Base):

    __tablename__ = "token"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, server_default=func.gen_random_uuid(), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(User, back_populates="tokens")

    @property
    def dict(self):
        return {
            "id": self.id,
            "token": self.token,
            "user": self.user.dict,
        }


class Article(Base):

    __tablename__ = "article"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(User, back_populates="articles")

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "owner": self.user_id,
            "created_at": self.created_at.isoformat(),
        }


MODEL_TYPE = Type[User | Token | Article]
MODEL = User | Token | Article

Base.metadata.create_all(bind=engine)