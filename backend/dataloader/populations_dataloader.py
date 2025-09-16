import pandas as pd

from exceptions.DataNotGeneratedException import DataNotGeneratedException
from helpers.csv_helpers import readCsv
from helpers.constants import *
from helpers.os_helpers import getGitRoot

POPULATION_TRENDS_FILENAME = "population_trends_by_county.csv"

FIPS_STRING_CONVERTER = {FIPS: str}

def get_population_trend_for_county(fips: str, county: str) -> pd.DataFrame:
    try:
        df = readCsv(f"{getGitRoot()}/{DEMOGRAPHICS_RESULTS_FILE_PATH}/{POPULATION_TRENDS_FILENAME}", converters=FIPS_STRING_CONVERTER)
        return df[df[FIPS] == fips]
    except FileNotFoundError:
        raise DataNotGeneratedException(county)

def get_population_trend_for_counties_in_state(state: str, state_fips: str) -> pd.DataFrame:
    try:
        df = readCsv(f"{getGitRoot()}/{DEMOGRAPHICS_RESULTS_FILE_PATH}/{POPULATION_TRENDS_FILENAME}", converters=FIPS_STRING_CONVERTER)
        return df[df[FIPS].str[:2] == state_fips]
    except FileNotFoundError:
        raise DataNotGeneratedException(state)
