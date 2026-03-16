from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from database import engine, create_db_and_tables


if __name__ == "__main__":
    #Session = sessionmaker(engine)

    #with Session as session:
    #    pass

    create_db_and_tables()



























