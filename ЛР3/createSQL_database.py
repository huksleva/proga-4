from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey
from sqlalchemy import create_engine


# Создаём наш реестр баз данных
class Base(DeclarativeBase):
    pass


class UserBase(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    created_at: Mapped[DATETIME] = mapped_column(nullable=True)


class Currency(Base):
    __tablename__ = "currency"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True, nullable=True)
    name: Mapped[str] = mapped_column()


class Subscription(Base):
    __tablename__ = "Subscription"
    user_id: Mapped[int] = mapped_column(ForeignKey("UserBase.id"))
    currency: Mapped[int] = mapped_column(ForeignKey("Currency.id"))







































