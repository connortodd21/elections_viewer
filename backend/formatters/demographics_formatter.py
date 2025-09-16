import pandas as pd

from exceptions.InputException import InvalidInputError
from helpers.constants import *

def format_county_results_into_state(data: pd.DataFrame) -> pd.DataFrame:
    """
    Given a dataframe of county-level results for a state, return the 
    summed values for each row
    """
    state_fips_codes = data[FIPS].str[:2].unique()
    
    if len(state_fips_codes) != 1:
        raise InvalidInputError("Data contains more than one state")

    state_fips = state_fips_codes[0]
    state_name = FIPS_TO_STATE[state_fips]

    # Group by YEAR and AGEGRP, sum numeric columns
    grouped = (
        data.drop(columns=["FIPS"])
          .groupby(["YEAR", "AGEGRP"], as_index=False)
          .sum(numeric_only=True)
    )
    
    # Add back the state FIPS
    grouped.insert(0, STATE, state_name)
    
    return grouped