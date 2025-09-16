import pandas as pd

from helpers.csv_helpers import readCsv
from helpers.constants import *
from helpers.os_helpers import getGitRoot

FIPS_STRING_CONVERTER = {FIPS: str}

def get_counties_by_state(state: str) -> pd.DataFrame:
    return readCsv(f"{getGitRoot()}/{COUNTIES_FILE_PATH.format(state)}/counties.csv", converters=FIPS_STRING_CONVERTER)

def get_county_by_fips(fips: str) -> pd.DataFrame:
    df = readCsv(f"{getGitRoot()}/{ALL_COUNTIES_FILE_PATH}/all_counties.csv", converters=FIPS_STRING_CONVERTER)
    return df[df[FIPS] == fips]

def get_county(county: str, fips:str) -> pd.DataFrame:
    df = readCsv(f"{getGitRoot()}/{ALL_COUNTIES_FILE_PATH}/all_counties.csv", converters=FIPS_STRING_CONVERTER)
    return df[(df[FIPS] == fips) & (df[NAME] == county)]