import pandas as pd

from common.defs import * 
from common.csv_helpers import *
from common.data_helpers import getCorrectOfficeCodes
from common.input_helpers import getStateInput
from common.os_helpers import getGitRoot

MI_RAW_DATA_FILE_NAME = "STATE_GENERAL_MI_CENR_BY_COUNTY"
GIT_ROOT = getGitRoot()

def getDataForYear(year: str, state: str) -> pd.DataFrame:
    return readData(f"{GIT_ROOT}/{RAW_DATA_FILE_PATH.format(state)}/{year}{MI_RAW_DATA_FILE_NAME}.txt").iloc[:, :-1][:-1]
    
def formatColumns(data: pd.DataFrame) -> pd.DataFrame:
    data["CandidateFullName"] = data["CandidateFirstName"] + " " + data["CandidateLastName"]
    return data

def dropUnusedColumns(data: pd.DataFrame) -> pd.DataFrame:
    data.drop(['DistrictCode(Text)', 'StatusCode', 'CountyCode', 'PartyOrder', 'CandidateFirstName', 'CandidateLastName', 'CandidateMiddleName', 'CandidateID', 'CandidateFormerName', 'WriteIn(W)/Uncommitted(Z)', 'Recount(*)'], axis=1, inplace=True)
    return data

def filterForStatewideElectionType(data: pd.DataFrame, year: str) -> pd.DataFrame:
    office_codes = getCorrectOfficeCodes(year)
    return data[data['OfficeCode(text)'].isin(list(office_codes.keys()))]

def filterOutWriteIns(data: pd.DataFrame) -> pd.DataFrame:
    return data[data['WriteIn(W)/Uncommitted(Z)'].isnull()]

def filterForOnlyDemocratOrRepublicanCandidates(data: pd.DataFrame) -> pd.DataFrame:
    return data[data['PartyDescription'].isin(PARTY_NAMES)]

"""
In the 2016-2022 datasets, Grand Traverse county is called Gd. Traverse
In the 2024 dataset, the county is renamed to Grand Traverse

In the 2016-2022 datasets, St. Clair and St. Joseph have a "." in the name
In the 2024 dataset, they do not

This method renames the called out counties in the 2016-2022 datasets to be uniform with the 2024 dataset
"""
def fixCountyNameData(data: pd.DataFrame) -> pd.DataFrame:
    grand_traverse_old = "GD. TRAVERSE"
    grand_traverse_new = "GRAND TRAVERSE"
    data[COUNTY_NAME].replace(grand_traverse_old, grand_traverse_new, inplace=True)

    st_clair_old = "ST. CLAIR"
    st_clair_new = "ST CLAIR"
    data[COUNTY_NAME].replace(st_clair_old, st_clair_new, inplace=True)

    st_joseph_old = "ST. JOSEPH"
    st_joseph_new = "ST JOSEPH"
    data[COUNTY_NAME].replace(st_joseph_old, st_joseph_new, inplace=True)

    return data

state = getStateInput()

years = ["2016", "2018", "2020", "2022", "2024"]
for year in years:
    data = getDataForYear(year, state)
    if year != 2024:
        data = fixCountyNameData(data)
    data = filterForStatewideElectionType(data, year)
    data = filterOutWriteIns(data)
    data = filterForOnlyDemocratOrRepublicanCandidates(data)
    data = formatColumns(data)
    data = dropUnusedColumns(data)
    writeDataFrameToCSV(f"{GIT_ROOT}/{PROCESSED_DATA_FILE_PATH.format(state)}/{year}_results.csv", data)
