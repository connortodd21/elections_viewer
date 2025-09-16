import pandas as pd

from exceptions.DataNotGeneratedException import DataNotGeneratedException
from helpers.csv_helpers import readCsv
from helpers.constants import *
from helpers.os_helpers import getGitRoot

DEMOGRAPHIC_TRENDS_FILENAME = "demographic_trends_by_county.csv"

FIPS_STRING_CONVERTER = {FIPS: str}

def get_demographic_trend_for_county(fips: str, county: str, state: str) -> pd.DataFrame:
    try:
        df = readCsv(f"{getGitRoot()}/{DEMOGRAPHICS_RESULTS_FILE_PATH}/{state}/{DEMOGRAPHIC_TRENDS_FILENAME}", converters=FIPS_STRING_CONVERTER)
        return df[df[FIPS] == fips]
    except FileNotFoundError:
        raise DataNotGeneratedException(county)

def get_demographic_trend_for_state(state: str) -> pd.DataFrame:
    try:
        df = readCsv(f"{getGitRoot()}/{DEMOGRAPHICS_RESULTS_FILE_PATH}/{state}/{DEMOGRAPHIC_TRENDS_FILENAME}", converters=FIPS_STRING_CONVERTER)
        return df
    except FileNotFoundError:
        raise DataNotGeneratedException(state)