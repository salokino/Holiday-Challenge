from datetime import datetime
from sqlalchemy import Boolean, CHAR, Integer, SmallInteger, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from typing import List

from sqlalchemy.orm.properties import ForeignKey


# base class
class Base(DeclarativeBase):
    pass


# table classes
class Airport(Base):
    __tablename__ = "airports"

    iata_code: Mapped[str] = mapped_column(CHAR(3), primary_key=True)
    location: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(String(128))

    @validates("iata_code")
    def validate_iata_code(self, key, code):
        if len(code) != 3:
            raise ValueError("IATA code has to be of length 3")
        return code


class Hotel(Base):
    __tablename__ = "hotels"

    hotel_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    hotel_name: Mapped[str] = mapped_column(String(128))
    hotel_stars: Mapped[int] = mapped_column(SmallInteger)

    offers: Mapped[List["Offer"]] = relationship(back_populates="hotel")


class Offer(Base):
    __tablename__ = "offers"

    offer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count_adults: Mapped[int] = mapped_column(SmallInteger)
    count_children: Mapped[int] = mapped_column(SmallInteger)
    duration: Mapped[int] = mapped_column(SmallInteger)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.hotel_id"))
    inbound_arrival_airport: Mapped[str] = mapped_column(CHAR(3))
    inbound_arrival_datetime: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    inbound_departure_airport: Mapped[str] = mapped_column(CHAR(3))
    inbound_departure_datetime: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    mealtype: Mapped[str] = mapped_column(String(32))
    oceanview: Mapped[bool] = mapped_column(Boolean)
    outbound_arrival_airport: Mapped[str] = mapped_column(CHAR(3))
    outbound_arrival_datetime: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    outbound_departure_airport: Mapped[str] = mapped_column(CHAR(3))
    outbound_departure_datetime: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    price: Mapped[int] = mapped_column(Integer)
    roomtype: Mapped[str] = mapped_column(String(32))

    hotel: Mapped["Hotel"] = relationship(back_populates="offers")


    @validates("inbound_arrival_airport")
    @validates("inbound_departure_airport")
    @validates("outbound_arrival_airport")
    @validates("outbound_departure_airport")
    def validate_airports(self, key, code):
        if len(code) != 3:
            raise ValueError("IATA code has to be of length 3")
        return code
