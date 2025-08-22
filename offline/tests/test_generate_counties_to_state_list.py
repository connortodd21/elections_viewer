import pandas as pd
import requests

from common.csv_helpers import readCsv
from common.data_helpers import generateCountyFipsRow
from common.defs import *
from common.os_helpers import getGitRoot
from generate_counties_to_state_list import cleanCountyNameFcc

state_map = {
    "01": AL, "02": AK, "04": AZ, "05": AR,
    "06": CA, "08": CO, "09": CT, "10": DE,
    "11": DC, "12": FL, "13": GA, "15": HI,
    "16": ID, "17": IL, "18": IN, "19": IA,
    "20": KS, "21": KY, "22": LA, "23": ME,
    "24": MD, "25": MA, "26": MI, "27": MN,
    "28": MS, "29": MO, "30": MT, "31": NE,
    "32": NV, "33": NH, "34": NJ, "35": NM,
    "36": NY, "37": NC, "38": ND, "39": OH,
    "40": OK, "41": OR, "42": PA, "44": RI,
    "45": SC, "46": SD, "47": TN, "48": TX,
    "49": UT, "50": VT, "51": VA, "53": WA,
    "54": WV, "55": WI, "56": WY
}

def testGenerateCountiesToStateList() -> None:
    # Generate a df containing {fips_code, state, county}
    resp = requests.get("https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt")

    lines = resp.text.strip().splitlines()
    expected = pd.DataFrame([])
    for i, line in enumerate(lines):
        if i > 71: # this is where the counties list begins
            parts = line.strip().split(None, 1)
            if len(parts) != 2:
                continue
            fips_code, county = parts
            if not fips_code.endswith("000"): # state fips codes end in 000 so skip those lines
                county = cleanCountyNameFcc(county)
                state = state_map.get(fips_code[:2], "Unknown")
                expected = pd.concat([expected, generateCountyFipsRow(county, state, fips_code)], ignore_index=True)

    # see https://www.cdc.gov/nchs/data/data_acces_files/County-Geography.pdf for AK transformations
    expected = expected[expected[NAME] != "Prince of Wales-Outer Ketchikan"] # transformed into Prince of Wales-Hyder in 2008
    expected = expected[expected[NAME] != "Skagway-Yakutat-Angoon"] # renamed to Skagway-Hoonah-Angoon in 1992
    expected = expected[expected[NAME] != "Skagway-Hoonah-Angoon"] # split to Hoonah-Angoon and Skagaway in 2007
    expected = expected[expected[NAME] != "Wrangell-Petersburg"] # renamed to Petersburg in 2008
    expected = expected[expected[NAME] != "Dade"] # renamed to Miami-Dade in 1997
    # see https://www.vdh.virginia.gov/content/uploads/sites/23/2016/05/TR-63-FIPS-Code-Chart-12-28-18.pdf for VA
    expected = expected[expected[NAME] != "South Boston"] # Now a town - part of Halifax as of 2018
    expected = expected[expected[NAME] != "Clifton Forge"] # Now a town - part of Alleghany as of 2018
    # name semantics
    expected.loc[expected[FIPS] == "17099", 'Name'] = "LaSalle" 
    expected.loc[expected[FIPS] == "18033", 'Name'] = "DeKalb" 
    expected.loc[expected[FIPS] == "18087", 'Name'] = "LaGrange" 
    expected.loc[expected[FIPS] == "18091", 'Name'] = "LaPorte" 
    expected.loc[expected[FIPS] == "19141", 'Name'] = "O'Brien" 
    expected.loc[expected[FIPS] == "24033", 'Name'] = "Prince George's" 
    expected.loc[expected[FIPS] == "24035", 'Name'] = "Queen Anne's" 
    expected.loc[expected[FIPS] == "24037", 'Name'] = "St. Mary's" 
    expected.loc[expected[FIPS] == "35011", 'Name'] = "De Baca" 
    expected.loc[expected[FIPS] == "42083", 'Name'] = "McKean" 
    # known issues with dataset. see https://github.com/connortodd21/elections_viewer/issues/3
    expected = expected[expected[NAME] != "Yellowstone National Park"] 
    # add newer counties not in gov dataset
    expected = pd.concat([expected, generateCountyFipsRow("Hoonah-Angoon", AK, "02105")])
    expected = pd.concat([expected, generateCountyFipsRow("Petersburg", AK, "02195")])
    expected = pd.concat([expected, generateCountyFipsRow("Prince of Wales-Hyder", AK, "02198")])
    expected = pd.concat([expected, generateCountyFipsRow("Skagway", AK, "02230")])
    expected = pd.concat([expected, generateCountyFipsRow("Wrangell", AK, "02275")])
    expected = pd.concat([expected, generateCountyFipsRow("Broomfield", CO, "08014")])
    expected = pd.concat([expected, generateCountyFipsRow("Miami-Dade", FL, "12086")])
    expected = pd.concat([expected, generateCountyFipsRow("Dade", GA, "13083")])
    expected = pd.concat([expected, generateCountyFipsRow("Dade", MO, "29057")])

    # Get my dataset
    actual = readCsv(f"{getGitRoot()}/{ALL_COUNTIES_FILE_PATH}/all_counties.csv", converters={'FIPS': str})

    # Compare expected to the data in all_counties.csv
    extra_in_actual = actual.merge(expected, how='left', indicator=True).query('_merge=="left_only"')
    missing_in_actual = expected.merge(actual, how='left', indicator=True).query('_merge=="left_only"')

    assert extra_in_actual.empty
    assert missing_in_actual.empty
    print("testGenerateCountiesToStateList passed!")