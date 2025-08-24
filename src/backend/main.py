from database import DatabaseClient
from dotenv import dotenv_values, load_dotenv
from fastapi import FastAPI, Depends
from query_builder import QueryBuilder
from schemas import HotelsSearchQueryAdvanced, HotelOfferResponse
from sqlalchemy.orm import Session
from typing import Annotated


load_dotenv()
config = dotenv_values(".env")

app = FastAPI()
db_client = DatabaseClient(url=f"postgresql://{config['USER']}:{config['PASSWORD']}"\
                               f"@{config['HOST']}:{config['PORT']}/{config['DB_NAME']}")

@app.get("/")
def read_root():
    return {}

@app.get("/offers/")
def read_hotes():
    return {}

@app.get("/hotels")
def search_hotels(
    query_params: Annotated[HotelsSearchQueryAdvanced, Depends()],
    session: Session = Depends(db_client.get_session)
    ) -> list[HotelOfferResponse]:
    """
    Endpoint to search for hotel offers based on various query parameters.
    The endpoint returns the cheapest offer of each hotel along with the count of offers per hotel
    and trip details.

    Parameters
    ----------
    query_params : HotelsSearchQueryAdvanced
        The query parameters for searching hotels.
    session : Session
        The SQLAlchemy session to use for the query.

    Returns
    -------
    List[HotelOfferResponse]
        A list of hotel offers matching the query parameters.
    """

    query_builder = QueryBuilder(query_params=query_params)
    query = query_builder.build_query()
    results = session.execute(query).all()

    response_objects = []

    # convert results to response objects
    for res in results:
        res = res._asdict()
        response_obj = HotelOfferResponse.model_validate(res)
        response_objects.append(response_obj)

    return response_objects
