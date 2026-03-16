from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from database import engine, create_db_and_tables
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)



@app.post("/users/")
async def create_user():
    pass




if __name__ == "__main__":
    #Session = sessionmaker(engine)

    #with Session as session:
    #    pass

    create_db_and_tables()



























