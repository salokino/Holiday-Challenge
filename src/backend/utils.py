from pandas import DataFrame
from pandas.io.parsers import TextFileReader

import pandas as pd


def get_airports(chunksize: int | None = None) -> DataFrame | TextFileReader:
    """
    Wrapper function for reading airports data.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the airports data from the .csv file.
    """

    return read_data(path="../../data/airports.csv", chunksize=chunksize)


def get_flight_durations(chunksize: int | None = None) -> DataFrame | TextFileReader:
    """
    Wrapper function for reading flight durations data.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the flight durations data from the .csv file.
    """

    return read_data(path="../../data/flight_durations.csv", chunksize=chunksize)


def get_hotels(chunksize: int | None = None) -> DataFrame | TextFileReader:
    """
    Wrapper function for reading hotels data.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the hotels data from the .csv file.
    """

    return read_data(path="../../data/hotels.csv", chunksize=chunksize)


def get_offers(chunksize: int | None = None) -> DataFrame | TextFileReader:
    """
    Wrapper function for reading offers data.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the offers data from the .csv file.
    """

    return read_data(path="../../data/offers.csv", chunksize=chunksize)


def read_data(path: str, chunksize: int | None = None) -> DataFrame | TextFileReader:
    """
    Reads a .csv file from the specified path and returns it as a pandas DataFrame.

    Parameters
    ----------
    path : str
        The file path to the csv file to be read.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the data from the .csv file.
    """

    return pd.read_csv(filepath_or_buffer=path, chunksize=chunksize, engine="c", sep=",")
