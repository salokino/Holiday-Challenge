from dotenv import dotenv_values, load_dotenv
from fastapi import FastAPI, Depends
from models import Offer
from query_builder import QueryBuilder
from schemas import HotelsSearchQueryAdvanced
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated

import datetime


load_dotenv()
config = dotenv_values(".env")

app = FastAPI()


@app.get("/")
def read_root():
    return {}

@app.get("/offers/")
def read_hotes():
    return {}

@app.get("/hotels")
def search_hotels(query_params: Annotated[HotelsSearchQueryAdvanced, Depends()]):
    query_builder = QueryBuilder(query_params=query_params)
    query = query_builder.build_query()

    engine = create_engine(url=f"postgresql://{config['USER']}:{config['PASSWORD']}"\
                               f"@{config['HOST']}:{config['PORT']}/{config['DB_NAME']}")

    sm = sessionmaker(bind=engine)
    session = sm()

    results = session.execute(query).all()

    for result in results:
       print(result)
       print("~~~~~~~~~~~~----------------------------------------------~~~~~~~~~~~~")

    print(len(results))

