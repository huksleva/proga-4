from sqlalchemy import create_engine
from models import (
    Base,
    UserBase,
    Currency,
    Subscription
)



DB_URL = 'sqlite:///db/database.db'
engine = create_engine(DB_URL, echo=True)


def create_db_and_tables() -> None:
	Base.metadata.create_all(engine)

