import pandas as pd

from helpers.csv_helpers import readCsv
from helpers.constants import *
from helpers.os_helpers import getGitRoot

def get_counties_by_state(state: str) -> pd.DataFrame:
    return readCsv(f"{getGitRoot()}/{COUNTIES_FILE_PATH.format(state)}/counties.csv")

def get_county(county: str, fips:str) -> pd.DataFrame:
    df = readCsv(f"{getGitRoot()}/{ALL_COUNTIES_FILE_PATH}/all_counties.csv", converters={FIPS: str})
    return df[(df[FIPS] == fips) & (df[NAME] == county)]