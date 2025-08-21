import pandas as pd

from helpers.csv_helpers import readCsv
from helpers.constants import *
from helpers.os_helpers import getGitRoot

def get_counties_by_state(state: str) -> pd.DataFrame:
    return readCsv(f"{getGitRoot()}/{COUNTIES_FILE_PATH.format(state)}/counties.csv")