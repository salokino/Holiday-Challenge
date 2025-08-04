from bs4 import BeautifulSoup
from pandas import DataFrame
from utils import get_offers

import pandas as pd
import re
import requests

URL = "https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_"


def get_airport_info_by_iata_code(IATA_code: str) -> dict[str, str] | None:
    """
    Fetches airport information from wikipedia based on the provided IATA code.
    Makes an HTTP request to a predefined URL, parses the HTML response to find the airport
    matching the given IATA code, and extracts the airport's name and country.

    Parameters
    ----------
    IATA_code : str
        The code of the airport from which the information is requested.

    Returns
    -------
    dict : str, str
        A dictionary containing the following keys:
                - "IATA": The IATA code of the airport (str).
                - "airport_name": The name of the airport (str).
                - "airport_country": The country where the airport is located (str).
        If the IATA code is not found, the function returns None.
    """

    page = requests.get(url=f"{URL}{IATA_code[0]}")
    soup = BeautifulSoup(markup=page.text, features="html")

    for row in soup.find_all(name="tr"):
        entry = str(row)

        # check if the current airport matches the IATA code
        if re.search(pattern=f"<td>{IATA_code}</td>", string=entry):
            match_soup = BeautifulSoup(markup=entry, features="html")
            values = match_soup.find_all(name="td")

            # extract airport name and country
            airport_name = str(values[2].text).removeprefix("<td>").removesuffix("</td>")
            airport_country = str(values[3].text).removeprefix("<td>").removesuffix("</td>")

            return {
                "IATA": IATA_code,
                "airport_name": airport_name,
                "airport_country": airport_country
            }



def get_all_airports_from_offers(offers: DataFrame) -> set[str]:
    """
    Extracts all IATA codes from the offers dataset.

    Parameters
    ----------
    offers : DataFrame
        A pandas DataFrame containing the offers data from the csv file.

    Returns
    -------
    set : str
        A set containing all IATA codes from the offers dataset.
    """

    IATA_codes = set()

    # get all airports
    inbound_airports_arrival = offers["inboundarrivalairport"]
    inbound_airports_departure = offers["inbounddepartureairport"]
    outbound_airports_arrival = offers["outboundarrivalairport"]
    outbound_airports_departure = offers["outbounddepartureairport"]

    # store airport IATA codes in set
    IATA_codes = IATA_codes.union(inbound_airports_arrival.to_list())
    IATA_codes = IATA_codes.union(inbound_airports_departure.to_list())
    IATA_codes = IATA_codes.union(outbound_airports_arrival.to_list())
    IATA_codes = IATA_codes.union(outbound_airports_departure.to_list())

    return IATA_codes


def store_airport_dataset(data: list[dict[str, str]]) -> None:
    """
    Stores the airport information in a .csv file.

    Parameters
    ----------
    data : list[dict[str, str]]
        The airport information including IATA code, name and location.

    Returns
    -------
    None
    """

    with open(file="./data/airports.csv", mode="w") as file:
        for airport in data:
            file.write(f'{airport["IATA"]},{airport["airport_name"]},"{airport["airport_country"]}"\n')


if __name__ == "__main__":
    offers: DataFrame = get_offers()
    IATA_codes = get_all_airports_from_offers(offers=offers)
    airport_dataset: list[dict[str, str]] = []

    for code in IATA_codes:
        airport_info = get_airport_info_by_iata_code(code)
        if airport_info:
            airport_dataset.append(airport_info)

    store_airport_dataset(data=airport_dataset)
