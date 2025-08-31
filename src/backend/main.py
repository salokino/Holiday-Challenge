from pydantic import Field
from database import DatabaseClient
from dotenv import dotenv_values, load_dotenv
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from query_builder import *
from schemas import *
from sqlalchemy.orm import Session
from typing import Annotated


load_dotenv()
config = dotenv_values(".env")

app = FastAPI()
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_client = DatabaseClient(url=f"postgresql://{config['USER']}:{config['PASSWORD']}"\
                               f"@{config['HOST']}:{config['PORT']}/{config['DB_NAME']}")

airport_query_builder = AirportQueryBuilder()

@app.get("/")
def read_root():
    return {}

@app.get("/airports")
def read_airports(session: Session = Depends(db_client.get_session)):
    query = airport_query_builder.get_airports()
    results = session.execute(query).all()

    response_objects = []

    for res in results:
        res = res._asdict()
        response_obj = AirportResponse.model_validate(res)
        response_objects.append(response_obj)

    return response_objects


@app.get("/available-hotels")
async def get_available_hotels(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    stars: Annotated[int | None, Query(ge=1, le=5)] = None,
    session: Session = Depends(db_client.get_session)
) -> list[HotelsResponse]:

    query_builder = HotelQueryBuilder(limit=limit, offset=offset, stars=stars)
    query = query_builder.get_hotels()

    results = session.execute(query).all()
    response_objects = []

    # convert results to response objects
    for res in results:
        res = res._asdict()
        response_obj = HotelsResponse.model_validate(res)
        response_objects.append(response_obj)

    return response_objects


@app.get("/flight-details/{offer_id}")
async def get_flight_details(
    offer_id: Annotated[int, Field(ge=1)],
    session: Session = Depends(db_client.get_session)
    ):
    query = airport_query_builder.get_flight_details(offer_id=offer_id)
    result = session.execute(query).first()
    if result:
        result = result._asdict()

    return result


@app.get("/offers/{hotel_id}")
async def get_hotel_offers(
    hotel_id: Annotated[int, Field(ge=1)],
    query_params: Annotated[HotelsSearchQueryAdvanced, Depends()],
    session: Session = Depends(db_client.get_session),
    offset: Annotated[int, Query(ge=0)] = 0,
    order_by: Annotated[str, Query()] = "",
    limit: Annotated[int, Query(ge=1, le=100)] = 20
    ) -> list[HotelOffersResponse]:
        """
        Endpoint to get offers for a specific hotel based on various query parameters.

        Parameters
        ----------
        hotel_id : str
            The ID of the hotel to get offers for.
        query_params : HotelsSearchQueryAdvanced
            The query parameters for filtering offers.
        session : Session
            The SQLAlchemy session to use for the query.

        Returns
        -------
        List[HotelOffersResponse]
            A list of offers for the specified hotel matching the query parameters.
        """

        query_builder = HotelOffersQueryBuilder(
             hotel_id=hotel_id, limit=limit, offset=offset, order_by=order_by, query_params=query_params)
        query = query_builder.build_query()

        results = session.execute(query).all()
        response_objects = []

        # convert results to response objects
        for res in results:
            res = res._asdict()
            response_obj = HotelOffersResponse.model_validate(res)
            response_objects.append(response_obj)

        return response_objects

@app.get("/hotels")
async def search_hotels(
    query_params: Annotated[HotelsSearchQueryAdvanced, Depends()],
    session: Session = Depends(db_client.get_session)
    ) -> list[CheapestHotelOfferResponse]:
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
    List[CheapestHotelOfferResponse]
        A list of hotel offers matching the query parameters.
    """

    query_builder = CheapestOffersQueryBuilder(query_params=query_params)
    query = query_builder.build_query()

    results = session.execute(query).all()

    response_objects = []

    # convert results to response objects
    for res in results:
        res = res._asdict()
        response_obj = CheapestHotelOfferResponse.model_validate(res)
        response_objects.append(response_obj)

    return response_objects
