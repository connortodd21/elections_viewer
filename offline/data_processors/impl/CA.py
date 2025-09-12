import pandas as pd

from common.defs import *
from common.csv_helpers import readCsv, writeDataFrameToCSV
from data_processors.data_processor import DataProcessor


# Raw data column names
CONTEST_ID = "CONTEST_ID"
ELECTION_DATE = "ELECTION_DATE"
PARTY_NAME = "PARTY_NAME"
COUNTY_NAME = "COUNTY_NAME"
VOTE_TOTAL = "VOTE_TOTAL"
CANDIDATE_NAME = "CANDIDATE_NAME"
CANDIDATE_ID = "CANDIDATE_ID"
# Party names in raw data
DEMOCRATIC = "Democratic"
REPUBLICAN = "Republican"
REPUBLICAN_TRUMP_2016 = "Republican,AmericanIndependent"

# Contest ID to name mapping
CONTEST_ID_TO_NAME = {
    "1": PRESIDENT,
    "2": SENATE,
    "3": GOVERNOR
}
# Contest name to ID mapping
CONTEST_NAME_TO_ID = {
    PRESIDENT: "1",
    SENATE: "2",
    GOVERNOR: "3"
}

# used to clean data
RAW_CONTEST_IDS = {
    # for 2016 and 2024, 010000000000 is the contest id for president
    10000000000: PRESIDENT,
    # for 2020, 10000000000 is the contest id for president
    10000000000: PRESIDENT,
    # for 2016, 100000000001 is the contest id for senate seat 1
    100000000001: SENATE,
    # for 2022, 1.00E+11 is the contest id for senate seat 1
    100000000000: SENATE,
    # for 2024, 100000000002 is the contest id for senate seat 2
    100000000002: SENATE,
    # for 2018, 020000000000 is the contest id for governor
    20000000000: GOVERNOR,
    # for 2022, 20000000000 is the contest id for governor
    20000000000: GOVERNOR,
}
PARTY_NAMES = set(["Democratic", "Republican"])

# columns for result df
YEAR = "year"
ELECTION = "election"

class CAStateWideElectionDataProcessor(DataProcessor):

    def __init__(self) -> None:
        self.intermediate_file_path = f"{self.GIT_ROOT}/{PROCESSED_DATA_FILE_PATH.format(self.getState())}/intermediate_results.csv"
        super().__init__(CA)

    def getRawData(self) -> pd.DataFrame:
        data = pd.DataFrame()
        columns = None
        isFirstPass = True
        skipRows = 0
        for year in ELECTION_YEARS_AFTER_TRUMP:
            yearDf = readCsv(f"{self.GIT_ROOT}/{RAW_DATA_FILE_PATH.format(self.getState())}/{year}.csv", names=columns, skiprows=skipRows, thousands=",")
            # this is necessary as column names changed in 2020
            # in 2016 and 2018 words were separated with an "_". For 2020 onwards they use a space
            if isFirstPass:
                columns = yearDf.columns
                isFirstPass = False
                skipRows = 1
            data = pd.concat([data, yearDf])

        return data

    def cleanData(self, data: pd.DataFrame) -> pd.DataFrame:

        # The contest id values are huge values (10000000000, 20000000000)
        # This method adjusts them to be single-digit values 
        def simplifyContestIdValue(data: pd.DataFrame) -> pd.DataFrame:
            for key, value in RAW_CONTEST_IDS.items():
                data[CONTEST_ID].replace(key, CONTEST_NAME_TO_ID[value], inplace=True)
            return data

        # Some years are denoted with 2 digits (ex: 22) and some with four digits (ex: 2022)
        # This method ensures all date values use four digit representation
        def normalizeElectionDate(data: pd.DataFrame) -> pd.DataFrame:
            data[ELECTION_DATE] = pd.to_datetime(data[ELECTION_DATE], errors='coerce')
            return data

        # Trump's party in 2016 is listed as "Republican,AmericanIndependent"
        # This method changes it to "Republican"
        def correctTrump2016PartyToRepublican(data: pd.DataFrame) -> pd.DataFrame:
            data[PARTY_NAME].replace(REPUBLICAN_TRUMP_2016, REPUBLICAN, inplace=True)
            return data

        return data.pipe(simplifyContestIdValue).pipe(normalizeElectionDate).pipe(correctTrump2016PartyToRepublican)

    def filterData(self, data: pd.DataFrame) -> pd.DataFrame:

        # only using democrat and republican candidates
        def filterForOnlyDemocratOrRepublicanCandidates(data: pd.DataFrame) -> pd.DataFrame:
            return data[data[PARTY_NAME].isin(PARTY_NAMES)]

        def filterForOnlyStatewideElections(data: pd.DataFrame) -> pd.DataFrame:
            return data[data[CONTEST_ID].isin(CONTEST_ID_TO_NAME.keys())]

        # 2016 and 2018 senate general was D vs D. Not so interesting
        def filter2016And2018SenateGeneral(data: pd.DataFrame) -> pd.DataFrame:
            senate_candidate_ids_2016_and_2018 = set([85, 289, 495, 516])
            return data[~data[CANDIDATE_ID].isin(senate_candidate_ids_2016_and_2018)]

        return data.pipe(filterForOnlyDemocratOrRepublicanCandidates).pipe(filterForOnlyStatewideElections).pipe(filter2016And2018SenateGeneral)

    def dropData(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.drop(["INCUMBENT_FLAG", "WRITE_IN_FLAG", "COUNTY_ID"], axis=1)

    def processData(self, data: pd.DataFrame) -> pd.DataFrame:
        county_by_county_results = pd.DataFrame(columns=[YEAR, ELECTION, COUNTY, RAW_VOTES_D, RAW_VOTES_R, D_CANDIDATE, R_CANDIDATE])
        counties = data[COUNTY_NAME].unique()
        for county in counties:
            # get data for county
            county_results = data[(data[COUNTY_NAME] == county)]
            # split by election date
            results_for_date = [d for _, d in county_results.groupby([ELECTION_DATE])]
            for result_for_date in results_for_date:
                # group by election type (to handle cases in which there are multiple elextions in the same year)
                elections = [d for _, d in result_for_date.groupby([CONTEST_ID])]
                for election in elections:
                    year = self.getYear(election)
                    r_results = election[election[PARTY_NAME] == REPUBLICAN]
                    d_results = election[election[PARTY_NAME] == DEMOCRATIC]
                    county_election_results = self.createCountyLevelResultsDataFrame(
                        year,
                        self.getElectionType(election, year),
                        county,
                        d_results[VOTE_TOTAL].iloc[0],
                        r_results[VOTE_TOTAL].iloc[0],
                        d_results[CANDIDATE_NAME].iloc[0],
                        r_results[CANDIDATE_NAME].iloc[0]
                    )
                    county_by_county_results = pd.concat([county_by_county_results, county_election_results])

        return county_by_county_results

    def writeDataToResults(self, data: pd.DataFrame) -> None:
        writeDataFrameToCSV(f"{self.GIT_ROOT}/{RESULTS_FILE_PATH.format(self.getState())}/statewide_results.csv", data.sort_values([YEAR, ELECTION]))

    ################################################################################
    #### Custom functions for this class
    ################################################################################

    # get the type of election (president, governor, senate)
    def getElectionType(self, data: pd.DataFrame, year: str) -> str:
        return CONTEST_ID_TO_NAME[data.head(1)[CONTEST_ID].iloc[0]]

    # given a dataframe, get the year from the first row
    def getYear(self, data: pd.DataFrame) -> str:
        return data[ELECTION_DATE].iloc[0].year
