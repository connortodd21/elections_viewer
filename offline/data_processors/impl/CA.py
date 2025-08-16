import pandas as pd

from common.defs import *
from common.csv_helpers import readCsv, writeDataFrameToCSV
from data_processors.data_processor import DataProcessor

class CAStateWideElectionDataProcessor(DataProcessor):

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

    def getState(self) -> str:
        return CA

    def getRawData(self) -> pd.DataFrame:
        data = pd.DataFrame()
        columns = None
        isFirstPass = True
        skipRows = 0
        for year in ELECTION_YEARS_AFTER_TRUMP:
            yearDf = readCsv(f"{self.GIT_ROOT}/{RAW_DATA_FILE_PATH.format(self.getState())}/{year}.csv", names=columns, skiprows=skipRows)
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
            for key, value in self.RAW_CONTEST_IDS.items():
                data[self.CONTEST_ID].replace(key, self.CONTEST_NAME_TO_ID[value], inplace=True)
            return data

        # Some years are denoted with 2 digits (ex: 22) and some with four digits (ex: 2022)
        # This method ensures all date values use four digit representation
        def normalizeElectionDate(data: pd.DataFrame) -> pd.DataFrame:
            data[self.ELECTION_DATE] = pd.to_datetime(data[self.ELECTION_DATE], errors='coerce')
            return data

        # Trump's party in 2016 is listed as "Republican,AmericanIndependent"
        # This method changes it to "Republican"
        def correctTrump2016PartyToRepublican(data: pd.DataFrame) -> pd.DataFrame:
            data[self.PARTY_NAME].replace(self.REPUBLICAN_TRUMP_2016, self.REPUBLICAN, inplace=True)
            return data

        return data.pipe(simplifyContestIdValue).pipe(normalizeElectionDate).pipe(correctTrump2016PartyToRepublican)

    def filterData(self, data: pd.DataFrame) -> pd.DataFrame:

        # only using democrat and republican candidates
        def filterForOnlyDemocratOrRepublicanCandidates(data: pd.DataFrame) -> pd.DataFrame:
            return data[data[self.PARTY_NAME].isin(self.PARTY_NAMES)]

        def filterForOnlyStatewideElections(data: pd.DataFrame) -> pd.DataFrame:
            return data[data[self.CONTEST_ID].isin(self.CONTEST_ID_TO_NAME.keys())]

        # 2016 and 2018 senate general was D vs D. Not so interesting
        def filter2016And2018SenateGeneral(data: pd.DataFrame) -> pd.DataFrame:
            senate_candidate_ids_2016_and_2018 = set([85, 289, 495, 516])
            return data[~data[self.CANDIDATE_ID].isin(senate_candidate_ids_2016_and_2018)]

        return data.pipe(filterForOnlyDemocratOrRepublicanCandidates).pipe(filterForOnlyStatewideElections).pipe(filter2016And2018SenateGeneral)

    def dropData(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.drop(["INCUMBENT_FLAG", "WRITE_IN_FLAG", "COUNTY_ID"], axis=1)

    def generateCountyByCountyResults(self, data: pd.DataFrame) -> pd.DataFrame:
        county_by_county_results = pd.DataFrame(columns=[self.YEAR, self.ELECTION, self.COUNTY, self.RAW_VOTES_D, self.RAW_VOTES_R, self.D_CANDIDATE, self.R_CANDIDATE])
        counties = data[self.COUNTY_NAME].unique()
        for county in counties:
            # get data for county
            county_results = data[(data[self.COUNTY_NAME] == county)]
            # split by election date
            results_for_date = [d for _, d in county_results.groupby([self.ELECTION_DATE])]
            for result_for_date in results_for_date:
                # group by election type (to handle cases in which there are multiple elextions in the same year)
                elections = [d for _, d in result_for_date.groupby([self.CONTEST_ID])]
                for election in elections:
                    year = self.getYear(election)
                    r_results = election[election[self.PARTY_NAME] == self.REPUBLICAN]
                    d_results = election[election[self.PARTY_NAME] == self.DEMOCRATIC]
                    county_election_results = pd.DataFrame({
                        self.YEAR: [year],
                        self.ELECTION: [self.getElectionType(election, year)],
                        self.COUNTY: [county],
                        self.RAW_VOTES_D: [d_results[self.VOTE_TOTAL].iloc[0]],
                        self.RAW_VOTES_R: [r_results[self.VOTE_TOTAL].iloc[0]],
                        self.D_CANDIDATE: [d_results[self.CANDIDATE_NAME].iloc[0]],
                        self.R_CANDIDATE: [r_results[self.CANDIDATE_NAME].iloc[0]]
                    })
                    county_by_county_results = pd.concat([county_by_county_results, county_election_results])

        return county_by_county_results

    def writeDataToResults(self, data: pd.DataFrame) -> None:
        writeDataFrameToCSV(f"{self.GIT_ROOT}/{RESULTS_FILE_PATH.format(self.getState())}/statewide_results.csv", data.sort_values([self.YEAR, self.ELECTION]))

    ################################################################################
    #### Custom functions for this class
    ################################################################################

    # get the type of election (president, governor, senate)
    def getElectionType(self, data: pd.DataFrame, year: str) -> str:
        return self.CONTEST_ID_TO_NAME[data.head(1)[self.CONTEST_ID].iloc[0]]

    # given a dataframe, get the year from the first row
    def getYear(self, data: pd.DataFrame) -> str:
        return data[self.ELECTION_DATE].iloc[0].year
