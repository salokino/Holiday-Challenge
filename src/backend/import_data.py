from models import Airport, Base, FlightDuration, Hotel, Offer
from dotenv import dotenv_values, load_dotenv
from pandas import DataFrame, to_datetime
from pandas.io.parsers.readers import TextFileReader
from utils import get_airports, get_flight_durations, get_hotels, get_offers
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session


load_dotenv(".env")
config = dotenv_values(".env")

def filter_offers_by_hotel_ids(hotel_ids: set[int], offers: DataFrame) -> DataFrame:
    return DataFrame(offers[offers["hotelid"].isin(list(hotel_ids))])


def get_hotel_ids(hotel_df: DataFrame | TextFileReader) -> set[int] | None:
    if isinstance(hotel_df, DataFrame):
        hotel_ids = set(hotel_df["hotelid"].unique())
        return hotel_ids


def import_airports(airport_df: DataFrame | TextFileReader, session: Session) -> None:
    airports: list[Airport] = []

    if isinstance(airport_df, DataFrame):
        for row in airport_df.itertuples():
            airport = Airport(
                iata_code=row.IATA_Code, # pyright: ignore[reportAttributeAccessIssue]
                location=row.Location, # pyright: ignore[reportAttributeAccessIssue]
                name=row.Airport_Name) # pyright: ignore[reportAttributeAccessIssue]
            airports.append(airport)

    if airports:
        session.add_all(airports)
        session.commit()


def import_flight_durations(flight_durations_df: DataFrame | TextFileReader, session: Session) -> None:
    flight_durations: list[FlightDuration] = []

    if isinstance(flight_durations_df, DataFrame):
        for row in flight_durations_df.itertuples():
            flight_duration = FlightDuration(
                arrival_airport=row.arrival_airport, # pyright: ignore[reportAttributeAccessIssue]
                departure_airport=row.departure_airport, # pyright: ignore[reportAttributeAccessIssue]
                duration=row.duration_in_minutes) # pyright: ignore[reportAttributeAccessIssue]
            flight_durations.append(flight_duration)

    if flight_durations:
        session.add_all(flight_durations)
        session.commit()


def import_hotels(hotel_df: DataFrame | TextFileReader, session: Session) -> None:
    hotels: list[Hotel] = []

    if isinstance(hotel_df, DataFrame):
        for row in hotel_df.itertuples():
            hotel = Hotel(
                hotel_id=row.hotelid, # pyright: ignore[reportAttributeAccessIssue]
                hotel_name=row.hotelname, # pyright: ignore[reportAttributeAccessIssue]
                hotel_stars=row.hotelstars # pyright: ignore[reportAttributeAccessIssue]
            )
            hotels.append(hotel)

    if hotels:
        session.add_all(hotels)
        session.commit()


def import_offers(engine: Engine, hotel_df: DataFrame | TextFileReader, offer_df: DataFrame | TextFileReader) -> None:

    if isinstance(offer_df, TextFileReader) and isinstance(hotel_df, DataFrame):
        hotel_ids = get_hotel_ids(hotel_df=hotel_df)
        for chunk in offer_df:
            # rename columns according to the attributes
            column_mapping = {
                "countadults": "count_adults",
                "countchildren": "count_children",
                "duration": "duration",
                "hotelid": "hotel_id",
                "inboundarrivalairport": "inbound_arrival_airport",
                "inboundarrivaldatetime": "inbound_arrival_datetime",
                "inbounddepartureairport": "inbound_departure_airport",
                "departuredate": "outbound_departure_datetime",
                "mealtype": "mealtype",
                "oceanview": "oceanview",
                "outboundarrivalairport": "outbound_arrival_airport",
                "outboundarrivaldatetime": "outbound_arrival_datetime",
                "outbounddepartureairport": "outbound_departure_airport",
                "returndate": "inbound_departure_datetime",
                "price": "price",
                "roomtype": "roomtype"
            }

            if hotel_ids:
                filtered_chunk = filter_offers_by_hotel_ids(hotel_ids=hotel_ids, offers=chunk)
                filtered_chunk = filtered_chunk.rename(columns=column_mapping)

                # calculate the duration of the vacation in days
                outbound_dates = to_datetime(filtered_chunk['outbound_departure_datetime'], utc=True, format="ISO8601", errors="coerce")
                inbound_dates = to_datetime(filtered_chunk['inbound_departure_datetime'], utc=True, format="ISO8601", errors="coerce")
                filtered_chunk["duration"] = (inbound_dates - outbound_dates).dt.days

                filtered_chunk.to_sql(name="offers", con=engine, index=False, if_exists="append")


def create_tables(engine: Engine) -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    engine = create_engine(url=f"postgresql://{config['USER']}:{config['PASSWORD']}"\
                               f"@{config['HOST']}:{config['PORT']}/{config['DB_NAME']}")
    create_tables(engine=engine)

    sm = sessionmaker(bind=engine)
    session = sm()

    airport_df = get_airports()
    flight_durations_df = get_flight_durations()
    hotel_df = get_hotels()
    offer_df = get_offers(chunksize=100000)

    import_airports(airport_df=airport_df, session=session)
    import_flight_durations(flight_durations_df=flight_durations_df, session=session)
    import_hotels(hotel_df=hotel_df, session=session)
    import_offers(engine=engine, hotel_df=hotel_df, offer_df=offer_df)
