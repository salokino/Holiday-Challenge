from datetime import date, datetime
from fastapi import Query
from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated, List

airport_type = Annotated[str, StringConstraints(pattern="[A-Z]{3}")]


class AirportResponse(BaseModel):
    model_config = {"from_attributes": True}

    iata_code: str
    name: str


class CheapestHotelOfferResponse(BaseModel):
    model_config = {"from_attributes": True}

    count_adults: int
    count_children: int
    duration: int
    hotel_id: int
    hotel_name: str
    hotel_stars: int
    mealtype: str
    price: int
    roomtype: str


class HotelOffersResponse(BaseModel):
    model_config = {"from_attributes": True}

    count_adults: int
    count_children: int
    duration: int
    hotel_name: str
    hotel_stars: int
    inbound_departure_datetime: datetime
    mealtype: str
    oceanview: bool
    offer_id: int
    outbound_departure_datetime: datetime
    price: int
    roomtype: str


class HotelsSearchQueryBasic(BaseModel):
    model_config = {"extra": "forbid"}

    adults: Annotated[int | None, Field(ge=0)] = None
    airport: Annotated[List[airport_type] | None, Field(Query(default=None))]
    children: Annotated[int | None, Field(ge=0)] = None
    duration: Annotated[int | None, Field(ge=0)] = None
    earliest_departure: Annotated[date | None, Field()] = None
    latest_return: Annotated[date | None, Field()] = None


class HotelsSearchQueryAdvanced(HotelsSearchQueryBasic):
    inbound_arrival_time: Annotated[str | None, Field(pattern="morning|afternoon|evening|night")] = None
    inbound_departure_time: Annotated[str | None, Field(pattern="morning|afternoon|evening|night")] = None
    mealtype: Annotated[str | None, Field(max_length=32)] = None
    oceanview: Annotated[bool | None, Field()] = None
    outbound_arrival_airport: Annotated[str | None, Field(pattern="[A-Z]{3}")] = None
    outbound_arrival_time: Annotated[str | None, Field(pattern="morning|afternoon|evening|night")] = None
    outbound_departure_time: Annotated[str | None, Field(pattern="morning|afternoon|evening|night")] = None
    price_max: Annotated[int | None, Field(ge=0)] = None
    price_min: Annotated[int | None, Field(ge=0)] = None
    roomtype: Annotated[str | None, Field(max_length=32)] = None
