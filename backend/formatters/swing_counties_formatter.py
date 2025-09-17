from typing import List

import pandas as pd

from helpers.constants import *
from services.counties import get_fips_for_county

def get_swing_counties(data: pd.DataFrame, state: str) -> List[str]:
    """
        Given state election results and a state, get the swing counties 
    """
    swing_counties = []

    # split election results by county
    results_for_counties = [d for _, d in data.groupby([COUNTY])]
    for results_for_county in results_for_counties:
        county = results_for_county[COUNTY].iloc[0]
        d_counties = results_for_county[results_for_county[RAW_VOTES_D] > results_for_county[RAW_VOTES_R]]
        r_counties = results_for_county[results_for_county[RAW_VOTES_D] < results_for_county[RAW_VOTES_R]]
        tie_counties = results_for_county[results_for_county[RAW_VOTES_D] == results_for_county[RAW_VOTES_R]]

        # if both parties won an election in this county, it is a swing county
        # in the case of a tie we will consider it a swing county
        if (len(d_counties) > 0 and len(r_counties) > 0) or (len(tie_counties) > 0):
            fips = get_fips_for_county(county, state)
            swing_counties.append({COUNTY: county, FIPS_LOWER: fips})
    
    return swing_counties