from datetime import datetime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)
from sqlalchemy import (
    DateTime,
    String,
    ForeignKey,
    PrimaryKeyConstraint
)




# Создаём наш реестр баз данных
class Base(DeclarativeBase):
    pass


class UserBase(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Currency(Base):
    __tablename__ = "currency"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class Subscription(Base):
    __tablename__ = "Subscription"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"), primary_key=True)

    # Составной первичный ключ (гарантирует уникальность пары)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'currency_id'),
    )









































