from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
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
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)

    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        back_populates="user"
    )


class Currency(Base):
    __tablename__ = "currency"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        back_populates="currency"
    )


class Subscription(Base):
    __tablename__ = "subscription"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"), primary_key=True)

    # Составной первичный ключ (гарантирует уникальность пары)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'currency_id'),
    )

    currency: Mapped["Currency"] = relationship("Currency", back_populates="subscriptions")
    user: Mapped["UserBase"] = relationship("UserBase", back_populates="subscriptions")









































