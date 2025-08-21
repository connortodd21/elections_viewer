import geonamescache
import pandas as pd

from common.defs import *
from common.csv_helpers import writeDataFrameToCSV
from common.input_helpers import getStateInput
from common.os_helpers import getGitRoot

state = getStateInput()

gc = geonamescache.GeonamesCache()
state_counties = pd.DataFrame()
counties = gc.get_us_counties()
for county in counties:
    if county['state'] == state:
        state_counties = pd.concat([state_counties, pd.DataFrame({
            "Name": [county['name'].split(" ")[0]],
            "State": [county['state']],
            "FIPS": [county['fips']]
        })])

county_path = f"{getGitRoot()}/{COUNTIES_FILE_PATH.format(state)}"
writeDataFrameToCSV(f"{county_path}/counties.csv", state_counties)