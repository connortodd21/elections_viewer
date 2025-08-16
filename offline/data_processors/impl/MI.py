import pandas as pd

from common.defs import *
from common.csv_helpers import readTsvAsCsv, writeDataFrameToCSV
from data_processors.data_processor import DataProcessor

class MIStateWideElectionDataProcessor(DataProcessor):

    # raw data file name
    MI_RAW_DATA_FILE_NAME = "STATE_GENERAL_MI_CENR_BY_COUNTY"

    # raw data column names
    COUNTY_NAME = "CountyName"
    ELECTION_DATE = "ElectionDate"
    OFFICE_CODE = "OfficeCode(text)"
    CANDIDATE_FULL_NAME = "CandidateFullName"
    CANDIDATE_VOTES = "CandidateVotes"
    PARTY_DESCRIPTION = "PartyDescription"
    PARTY_NAMES = ["Democratic", "Republican", "DEMOCRATIC", "REPUBLICAN"]
    REPUBLICAN = ["Republican", "REPUBLICAN"]
    DEMOCRAT = ["Democratic", "DEMOCRATIC"]
    # office code mappings in raw datasets from 2016-2022
    OFFICE_CODES_OLD = {
        "1": PRESIDENT,
        "2": GOVERNOR,
        "5": SENATE
    }
    # office code mappings in raw datasets in 2024
    OFFICE_CODES_NEW = {
        "1": PRESIDENT,
        "2": GOVERNOR,
        "7": SENATE
    }
    
    def getState(self) -> str:
        return MI

    def getRawData(self) -> pd.DataFrame:
        data = pd.DataFrame()
        for year in ELECTION_YEARS_AFTER_TRUMP:
            yearDf = readTsvAsCsv(f"{self.GIT_ROOT}/{RAW_DATA_FILE_PATH.format(self.getState())}/{year}{self.MI_RAW_DATA_FILE_NAME}.txt").iloc[:, :-1][:-1]
            data = pd.concat([data, yearDf])
        return data
    
    def cleanData(self, data: pd.DataFrame) -> pd.DataFrame:
        # combine first/last names
        def addFirstNameColumn(data: pd.DataFrame) -> pd.DataFrame:
            data["CandidateFullName"] = data["CandidateFirstName"] + " " + data["CandidateLastName"]
            return data

        def fixCountyNameData(data: pd.DataFrame) -> pd.DataFrame:
            """
            In the 2016-2022 datasets, Grand Traverse county is called Gd. Traverse
            In the 2024 dataset, the county is renamed to Grand Traverse

            In the 2016-2022 datasets, St. Clair and St. Joseph have a "." in the name
            In the 2024 dataset, they do not

            This method renames the called out counties in the 2016-2022 datasets to be uniform with the 2024 dataset
            """
            grand_traverse_old = "GD. TRAVERSE"
            grand_traverse_new = "GRAND TRAVERSE"
            data[self.COUNTY_NAME].replace(grand_traverse_old, grand_traverse_new, inplace=True)

            st_clair_old = "ST. CLAIR"
            st_clair_new = "ST CLAIR"
            data[self.COUNTY_NAME].replace(st_clair_old, st_clair_new, inplace=True)

            st_joseph_old = "ST. JOSEPH"
            st_joseph_new = "ST JOSEPH"
            data[self.COUNTY_NAME].replace(st_joseph_old, st_joseph_new, inplace=True)
            return data

        return data.pipe(addFirstNameColumn).pipe(fixCountyNameData)

    def filterData(self, data: pd.DataFrame) -> pd.DataFrame:
        # only use statewide elections
        def filterForStatewideElectionType(data: pd.DataFrame) -> pd.DataFrame:
            # the pre-2024 and 2024 datasets use different election type ids
            election_dates_pre_2024 = set(['2016-11-08', '2018-11-06', '2020-11-03', '2022-11-08']) 
            election_date_2024 = '2024-11-05'
            old_data = data[(data['OfficeCode(text)'].isin(self.OFFICE_CODES_OLD)) & (data[self.ELECTION_DATE].isin(election_dates_pre_2024))]
            new_data = data[(data['OfficeCode(text)'].isin(self.OFFICE_CODES_NEW)) & (data[self.ELECTION_DATE] == election_date_2024)]
            return pd.concat([old_data, new_data])

        # filter out write in votes
        def filterOutWriteIns(data: pd.DataFrame) -> pd.DataFrame:
            return data[data['WriteIn(W)/Uncommitted(Z)'].isnull()]

        # only using democrat and republican candidates
        def filterForOnlyDemocratOrRepublicanCandidates(data: pd.DataFrame) -> pd.DataFrame:
            return data[data['PartyDescription'].isin(self.PARTY_NAMES)]
        
        return data.pipe(filterOutWriteIns).pipe(filterForOnlyDemocratOrRepublicanCandidates).pipe(filterForStatewideElectionType)


    def dropData(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.drop(['DistrictCode(Text)', 'StatusCode', 'CountyCode', 'PartyOrder', 'CandidateFirstName', 'CandidateLastName', 'CandidateMiddleName', 'CandidateID', 'CandidateFormerName', 'WriteIn(W)/Uncommitted(Z)', 'Recount(*)'], axis=1)

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
                elections = [d for _, d in result_for_date.groupby([self.OFFICE_CODE])]
                for election in elections:
                    year = self.getYear(election)
                    r_results = election[election[self.PARTY_DESCRIPTION].isin(self.REPUBLICAN)]
                    d_results = election[election[self.PARTY_DESCRIPTION].isin(self.DEMOCRAT)]
                    county_election_results = pd.DataFrame({
                        self.YEAR: [year],
                        self.ELECTION: [self.getElectionType(election, year)],
                        self.COUNTY: [county],
                        self.RAW_VOTES_D: [d_results[self.CANDIDATE_VOTES].iloc[0]],
                        self.RAW_VOTES_R: [r_results[self.CANDIDATE_VOTES].iloc[0]],
                        self.D_CANDIDATE: [d_results[self.CANDIDATE_FULL_NAME].iloc[0]],
                        self.R_CANDIDATE: [r_results[self.CANDIDATE_FULL_NAME].iloc[0]]
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
        office_codes = self.OFFICE_CODES_NEW if year == "2024" else self.OFFICE_CODES_OLD
        office_code = data.head(1)[self.OFFICE_CODE].iloc[0]
        return office_codes[str(office_code)]

    # given a dataframe, get the year from the first row
    def getYear(self, data: pd.DataFrame) -> str:
        return data[self.ELECTION_DATE].iloc[0].split("-")[0]
