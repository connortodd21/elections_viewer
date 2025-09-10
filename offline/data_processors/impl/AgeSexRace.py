import pandas as pd

from common.defs import *
from common.csv_helpers import readCsv
from data_processors.data_processor import DataProcessor


class AgeSexRaceDataProcessor(DataProcessor):

    DEMOGRAPHICS_2010_TO_2020_FILE_NAME = "co-est2020-alldata"
    DEMOGRAPHICS_2021_TO_2024_FILE_NAME = "co-est2024-alldata"

    def __init__(self, state: str) -> None:
        self.state = state
        super().__init__()
    
    def getState(self) -> str:
        return self.state

    def getRawData(self) -> pd.DataFrame:
        data = pd.DataFrame()

        # census data is divided into pre 2010-2020 and 2021-2024 datasets. need to read from both and concat
        census_2010_to_2020_data = readCsv(f"{self.GIT_ROOT}/{DEMOGRAPHICS_FILE_PATH}/{self.DEMOGRAPHICS_2010_TO_2020_FILE_NAME}.csv",encoding='latin1')
        census_2021_to_2024_data = readCsv(f"{self.GIT_ROOT}/{DEMOGRAPHICS_FILE_PATH}/{self.DEMOGRAPHICS_2021_TO_2024_FILE_NAME}.csv",encoding='latin1')
        data = pd.merge(census_2010_to_2020_data, census_2021_to_2024_data, on=["SUMLEV","REGION","DIVISION","STATE","COUNTY","STNAME","CTYNAME"], how='inner')
        return data

    def filterData(self, data: pd.DataFrame) -> pd.DataFrame:
        pass
    
    def cleanData(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def dropData(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def processData(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def writeDataToResults(self, data: pd.DataFrame) -> None:
        pass