import pandas as pd

from exceptions.DataNotGeneratedException import DataNotGeneratedException
from helpers.csv_helpers import readCsv
from helpers.constants import *
from helpers.os_helpers import getGitRoot

def get_election_results_for_county(county: str, state: str) -> pd.DataFrame:
    try:
        df = readCsv(f"{getGitRoot()}/{RESULTS_FILE_PATH.format(state)}/statewide_results.csv")
        return df[df[COUNTY] == county]
    except FileNotFoundError:
        raise DataNotGeneratedException(county)

def get_election_results_for_county_and_year(county: str, state: str, year: str) -> pd.DataFrame:
    try:
        df = readCsv(f"{getGitRoot()}/{RESULTS_FILE_PATH.format(state)}/statewide_results.csv", converters={YEAR: str})
        return df[(df[COUNTY] == county) & (df[YEAR] == year)]
    except FileNotFoundError:
        raise DataNotGeneratedException(county)

def get_statewide_election_years_for_county(county: str, state: str) -> pd.DataFrame:
    try:
        df = readCsv(f"{getGitRoot()}/{RESULTS_FILE_PATH.format(state)}/statewide_results.csv")
        return df[YEAR].unique()
    except FileNotFoundError:
        raise DataNotGeneratedException(county)