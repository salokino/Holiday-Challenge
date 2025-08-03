from pandas import DataFrame

import pandas as pd


def get_airports() -> DataFrame:
    """
    Wrapper function for reading airports data.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the airports data from the .csv file.
    """

    return read_data(path="./data/airports.csv")

def get_hotels() -> DataFrame:
    """
    Wrapper function for reading hotels data.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the hotels data from the .csv file.
    """

    return read_data(path="./data/hotels.csv")


def get_offers() -> DataFrame:
    """
    Wrapper function for reading offers data.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the offers data from the .csv file.
    """

    return read_data(path="./data/offers.csv")


def read_data(path: str) -> DataFrame:
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

    return pd.read_csv(filepath_or_buffer=path)
