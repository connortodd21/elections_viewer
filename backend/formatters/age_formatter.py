import pandas as pd

from exceptions.InputException import InvalidInputError
from helpers.constants import *

def format_demographic_results_into_age_results_for_county(data: pd.DataFrame) -> pd.DataFrame:
    """
    Given a dataframe of demographic data, return a new dataframe with age groups as columns for each county
    All rows must have FIPS codes for the same state        
    """
    state_fips_codes = data[FIPS].str[:2].unique()
    
    if len(state_fips_codes) != 1:
        raise InvalidInputError("Data contains more than one state")

    # Pivot the DataFrame so AGEGRP becomes columns
    data_new = data.pivot_table(
        index=[YEAR_UPPER, FIPS], 
        columns=AGEGRP, 
        values=TOT_POP
    ).reset_index()

    return data_new

def format_demographic_results_into_age_results_for_state(data: pd.DataFrame) -> pd.DataFrame:
    """
    Given a dataframe of demographic data, return a new dataframe with age groups as columns the state
    All rows must have FIPS codes for the same state
    """
    state_fips_codes = data[FIPS].str[:2].unique()
    
    if len(state_fips_codes) != 1:
        raise InvalidInputError("Data contains more than one state")

    data_new = data.pivot_table(
        index=[YEAR_UPPER, FIPS],
        columns=AGEGRP,
        values=TOT_POP,
        aggfunc="sum"   # In case there are duplicates
    ).reset_index()
    
    data_new.columns.name = None

    age_group_cols = data_new.columns.difference([YEAR_UPPER, FIPS])
    
    # Sum all FIPS rows for each year
    df_state_sum = data_new.groupby(YEAR_UPPER)[age_group_cols].sum().reset_index()
    
    return df_state_sum