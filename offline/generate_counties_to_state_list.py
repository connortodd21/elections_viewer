import geonamescache
import pandas as pd
import re

from common.csv_helpers import writeDataFrameToCSV
from common.data_helpers import generateCountyFipsRow
from common.defs import *
from common.os_helpers import getGitRoot

def cleanCountyNameFcc(name: str) -> str:
    """
    Standardize county names to match FCC's fips.txt
    """

    counties_with_city_in_name = {"Carson City", "Charles City", "James City"}

    # Remove any parentheses containing:
    # - created after <year>
    # - after <year>
    # - <year> Census Area
    name = re.sub(
        r"\(\s*.*?(created after|after \d{4}|\d{4} Census Area).*?\)", 
        "", 
        name, 
        flags=re.IGNORECASE
    )

    # Suffixes to remove iteratively from the end
    suffixes = [
        r"City and",
        r"and",
        r"County",
        r"Borough",
        r"Municipality",
        r"Census",
        r"Census Area"
    ]

    prev_name = None
    while name != prev_name:
        prev_name = name
        for suffix in suffixes:
            name = re.sub(rf"\b{suffix}\b\s*$", "", name).strip()

    # Remove trailing "City"/"city" if not in whitelist
    if re.search(r"\b[Cc]ity\b$", name) and name.strip() not in counties_with_city_in_name:
        name = re.sub(r"\b[Cc]ity\b$", "", name).strip()

    # Collapse multiple spaces
    name = re.sub(r"\s+", " ", name).strip()

    return name

gc = geonamescache.GeonamesCache()
counties = gc.get_us_counties()

all_counties = pd.DataFrame([])

for county in counties:
    state = county['state']
    fips = county['fips']
    name = county['name']
    if state in VALID_US_STATES:
        name = cleanCountyNameFcc(name)
        all_counties = pd.concat([all_counties, generateCountyFipsRow(name, state, str(fips))])

county_path = f"{getGitRoot()}/{ALL_COUNTIES_FILE_PATH}"
writeDataFrameToCSV(f"{county_path}/all_counties.csv", all_counties)