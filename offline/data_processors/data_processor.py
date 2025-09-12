import pandas as pd

from abc import ABC, abstractmethod

from common.defs import *
from common.csv_helpers import writeDataFrameToCSV
from common.os_helpers import getGitRoot

class DataProcessor(ABC):

    GIT_ROOT = getGitRoot()

    def __init__(self, state=None) -> None:
        self.state = state
        super().__init__()

    def getState(self) -> str:
        return self.state

    @abstractmethod
    def getRawData(self) -> pd.DataFrame:
        """
        Get all raw data for an election
        
        Return as a dataframe
        """
        pass

    @abstractmethod    
    def filterData(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Perform custom filtering for data

        Return dataframe with filtered data
        """
        pass

    @abstractmethod
    def cleanData(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Perform data cleaning actions such as filling N/As, fixing names, and normalizing

        Return dataframe with cleaned data
        """
        pass

    @abstractmethod
    def dropData(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Drop all unnecessary columns and/or rows

        Return dataframe without dropped data
        """
        pass

    @abstractmethod
    def processData(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Process data. Any custom operations and logic should go here

        Return dataframe after processing
        """
        pass

    @abstractmethod
    def writeDataToResults(self, data: pd.DataFrame) -> None:
        """
        Write the given dataframe to the results database. Result will be written as a csv
        """
        pass

    def setIntermediateData(self, data: pd.DataFrame) -> None:
        """
        Set the intermediate dataset. This will only be used if writeIntermediateDataset() is called
        """
        self.intermediate_data = data
    
    def writeIntermediateDataset(self) -> None:
        """
        Write the intermediate data to the intermediate file path, if both exist
        """
        if self.intermediate_data is not None and self.intermediate_file_path is not None:
            writeDataFrameToCSV(self.intermediate_file_path, self.intermediate_data)

    def createCountyLevelResultsDataFrame(
        self, 
        year: str, 
        election_type: str,
        county: str,
        democrat_vote_total: int,
        republican_vote_total: int,
        democrat_candidate_name: str,
        republican_candidate_name: str
    ) -> pd.DataFrame:
        """
        Create the county level dataframe during generateCountyByCountyResults
        """
        return pd.DataFrame({
            self.YEAR: [year],
            self.ELECTION: [election_type],
            self.COUNTY: [county],
            self.RAW_VOTES_D: [democrat_vote_total],
            self.RAW_VOTES_R: [republican_vote_total],
            self.D_CANDIDATE: [democrat_candidate_name],
            self.R_CANDIDATE: [republican_candidate_name]
        })
