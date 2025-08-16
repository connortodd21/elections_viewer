import pandas as pd

from abc import ABC, abstractmethod

from common.defs import *
from common.os_helpers import getGitRoot

class DataProcessor(ABC):

    GIT_ROOT = getGitRoot()

    @abstractmethod
    def getState(self) -> str:
        pass

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
    def generateCountyByCountyResults(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate election results for each county
        """
        pass

    @abstractmethod
    def setIntermediateData(self, data: pd. DataFrame) -> None:
        """
        Set the intermediate dataset. This will only be used if writeIntermediateDataset() is called
        """
        pass

    @abstractmethod
    def writeIntermediateDataset(self) -> None:
        """
        Write indermediate data to the "processed" folder
        """
        pass

    @abstractmethod
    def writeDataToResults(self, data: pd.DataFrame) -> None:
        """
        Write the given dataframe to the results database. Result will be written as a csv
        """
        pass