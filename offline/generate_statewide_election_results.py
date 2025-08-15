import pandas as pd

from common.defs import *
from common.csv_helpers import writeDataFrameToCSV
from common.data_helpers import getCorrectOfficeCodes
from common.input_helpers import getStateInput
from common.os_helpers import getGitRoot

GIT_ROOT = getGitRoot()

def getElectionType(data: pd.DataFrame, year: str) -> str:
    office_codes = getCorrectOfficeCodes(year)
    office_code = data.head(1)[OFFICE_CODE].iloc[0]
    return office_codes[str(office_code)]

# get list of all county names
counties = pd.DataFrame(columns=[COUNTY])
def initialize_county_list(data: pd.DataFrame) -> None:
    global counties 
    counties = data[COUNTY_NAME].unique()

state = getStateInput()

county_by_county_results = pd.DataFrame(columns=[YEAR, ELECTION, COUNTY, RAW_VOTES_D, RAW_VOTES_R, D_CANDIDATE, R_CANDIDATE])

years = ["2016", "2018", "2020", "2022", "2024"]
isCountyListInitialized = False


for year in years:
    results = pd.read_csv(f"{GIT_ROOT}/{PROCESSED_DATA_FILE_PATH.format(state)}/{year}_results.csv")
    if not isCountyListInitialized:
        initialize_county_list(results)
        isCountyListInitialized = True

    for county in counties:
        county_results = results[(results[COUNTY_NAME] == county)]
        # group by election type (to handle cases in which there are multiple elextions in the same year)
        elections = [d for _, d in county_results.groupby([OFFICE_CODE])]
        for election in elections:
            r_results = election[election[PARTY_DESCRIPTION].isin(REPUBLICAN)]
            d_results = election[election[PARTY_DESCRIPTION].isin(DEMOCRAT)]
            county_election_results = pd.DataFrame({
                YEAR: [year],
                ELECTION: [getElectionType(election, year)],
                COUNTY: [county],
                RAW_VOTES_D: [d_results[CANDIDATE_VOTES].iloc[0]],
                RAW_VOTES_R: [r_results[CANDIDATE_VOTES].iloc[0]],
                D_CANDIDATE: [d_results[CANDIDATE_FULL_NAME].iloc[0]],
                R_CANDIDATE: [r_results[CANDIDATE_FULL_NAME].iloc[0]]
            })
            county_by_county_results = pd.concat([county_by_county_results, county_election_results])
writeDataFrameToCSV(f"{GIT_ROOT}/{RESULTS_FILE_PATH.format(state)}/statewide_results.csv", county_by_county_results.sort_values([YEAR, ELECTION]))