from typing import List

import pandas as pd

from helpers.constants import *

def get_swing_counties(data: pd.DataFrame) -> List[str]:
    swing_counties = []

    # split election results by county
    results_for_counties = [d for _, d in data.groupby([COUNTY])]
    for results_for_county in results_for_counties:
        county = results_for_county[COUNTY].iloc[0]
        d_counties = results_for_county[results_for_county[RAW_VOTES_D] > results_for_county[RAW_VOTES_R]]
        r_counties = results_for_county[results_for_county[RAW_VOTES_D] < results_for_county[RAW_VOTES_R]]
        tie_counties = results_for_county[results_for_county[RAW_VOTES_D] == results_for_county[RAW_VOTES_R]]

        # if both parties won an election in this county, it is a swing county
        if len(d_counties) > 0 and len(r_counties) > 0:
            swing_counties.append(county)

        # in the case of a tie we will consider it a swing county
        if len(tie_counties) > 0:
            swing_counties.append(county)
    
    return swing_counties