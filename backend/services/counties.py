import pandas as pd

from dataloader.counties_dataloader import get_counties_by_state
from helpers.constants import *

def get_fips_for_county(county: str, state: str) -> str:
    """
        Given a county and state, get the corresponding fips code
    """
    counties_in_state = get_counties_by_state(state)
    return str(counties_in_state[counties_in_state[NAME] == county][FIPS].iloc[0])