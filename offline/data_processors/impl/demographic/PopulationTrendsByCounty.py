import pandas as pd

from common.defs import *
from common.csv_helpers import readCsv, writeDataFrameToCSV
from data_processors.data_processor import DataProcessor

# Raw data file paths
POPULATION_TRENDS_2010_TO_2020_FILE_NAME = "co-est2020-alldata"
POPULATION_TRENDS_2020_TO_2024_FILE_NAME = "co-est2024-alldata"

# Raw data column names without years
STATE_RAW = "STATE"
COUNTY_RAW = "COUNTY"
SUMLEV_RAW = "SUMLEV"
POPESTIMATE_RAW = "POPESTIMATE"
BIRTHS_RAW = "BIRTHS"
DEATHS_RAW = "DEATHS"
INTERNATION_MIGRATION_RAW = "INTERNATIONALMIG"
DOMESTIC_MIGRATION_RAW = "DOMESTICMIG"
NET_MIGRATION_RAW = "NETMIG"
RESIDUAL_RAW = "RESIDUAL"

class PopulationTrendsByCountyDataProcessor(DataProcessor):

    def __init__(self) -> None:
        self.intermediate_file_path = f"{self.GIT_ROOT}/{DEMOGRAPHICS_INTERMIEDIATE_FILE_PATH}/intermediate_results.csv"
        super().__init__()

    def getRawData(self) -> pd.DataFrame:
        # census data is divided into pre 2010-2020 and 2020-2024 datasets. need to read from both and concat
        encoding = "latin1" # needed to avoid encoding error when reading csv
        converters = {STATE_RAW: str, COUNTY_RAW: str}
        census_2010_to_2020_data = readCsv(f"{self.GIT_ROOT}/{DEMOGRAPHICS_RAW_FILE_PATH}/{POPULATION_TRENDS_2010_TO_2020_FILE_NAME}.csv",encoding=encoding,converters=converters)
        census_2020_to_2024_data = readCsv(f"{self.GIT_ROOT}/{DEMOGRAPHICS_RAW_FILE_PATH}/{POPULATION_TRENDS_2020_TO_2024_FILE_NAME}.csv",encoding=encoding,converters=converters)
        data = pd.merge(census_2010_to_2020_data, census_2020_to_2024_data, on=["SUMLEV","REGION","DIVISION","STATE","COUNTY","STNAME","CTYNAME"], how='inner')
        return data

    def filterData(self, data: pd.DataFrame) -> pd.DataFrame:
        # only use rows where sumlev=50 (indicating county)
        def filter_for_only_county_level(data: pd.DataFrame) -> pd.DataFrame:
            return data[data[SUMLEV_RAW] == 50]

        return data.pipe(filter_for_only_county_level)
    
    def cleanData(self, data: pd.DataFrame) -> pd.DataFrame:

        # combine state + county fips into one code
        def combine_fips(data: pd.DataFrame) -> pd.DataFrame:
            data[FIPS] = data[STATE_RAW].str.pad(width=2, side='left', fillchar='0') + data[COUNTY_RAW].str.pad(width=3, side='left', fillchar='0')
            column_to_move = data.pop(FIPS)
            data.insert(0, FIPS, column_to_move) # Insert it at index 0
            return data

        # during the merge of the two datasets, columns with the same name are appended with a "_y" for the 2020-2024 data
        # we will be using this data, so we can remove the _y and keep the original column name
        def remove_y(data: pd.DataFrame) -> pd.DataFrame:
            columns = list(data.columns)
            renamed_columns = {}
            suffix = "_y"
            for column in columns:
                if suffix in column:
                    renamed_columns[column] = column.split('_')[0]
            return data.rename(columns=renamed_columns)
        
        return data.pipe(combine_fips).pipe(remove_y)

    def dropData(self, data: pd.DataFrame) -> pd.DataFrame:
        # drop columns with demographic data before 2016
        def drop_unused_years(data: pd.DataFrame) -> pd.DataFrame:
            drop_columns = []
            years_to_drop = ["2010", "2011", "2012", "2013", "2014", "2015"]
            columns = list(data.columns)
            for year in years_to_drop:
                for column in columns:
                    if year in column:
                        drop_columns.append(column)
            return data.drop(drop_columns, axis=1)

        # these columns are unnecessary
        def drop_unnecessary_descriptors(data: pd.DataFrame) -> pd.DataFrame:
            drop_columns = [STATE_RAW, COUNTY_RAW, SUMLEV_RAW, "REGION", "DIVISION", "STNAME", "CTYNAME"]
            return data.drop(drop_columns, axis=1)

        # we dont need columns which measure rates or group data
        def drop_yearly_columns(data: pd.DataFrame) -> pd.DataFrame:
            drop_columns = []
            change_column_prefixes = [
                "NPOPCHG", # Numeric change in resident total population
                "RNATURALCHG", # Natural change rate in period 
                "RINTERNATIONALMIG", # Net international migration rate in period
                "RDOMESTICMIG", # Net domestic migration rate in period
                "RNETMIG", # Net migration rate in period
                "RDEATH", # Death rate in period 
                "RBIRTH", # Birth rate in period,
                "RNATURALINC", # Natural increase rate in period 
                "GQESTIMATES", # Group quarters total population estimate
                "NATURALINC", # Natural increase in period
                "NATURALCHG", # Natural change in period
                "RESIDUAL", # Residual for period. Used when calculating change and ratess
            ]
            columns = list(data.columns)
            for prefix in change_column_prefixes:
                for column in columns:
                    if prefix in column:
                        drop_columns.append(column)
            return data.drop(drop_columns, axis=1)

        # in the 2010-2020 dataset, 2020 data is estimated 
        # the 2020-2024 dataset contains real 2020 data
        # when merging these dataframes earlier, pandas adds a _x the left dataframe (2010-2020 data) for 2020 data
        # we will use the 2020-2024 dataset for 2020, so we can remove this dupe column
        def drop_2020_x_columns(data: pd.DataFrame) -> pd.DataFrame:
            drop_columns = []
            columns = list(data.columns)
            suffix = "_x"
            for column in columns:
                if suffix in column:
                    drop_columns.append(column)
            return data.drop(drop_columns, axis=1)        

        return data.pipe(drop_unused_years).pipe(drop_unnecessary_descriptors).pipe(drop_yearly_columns).pipe(drop_2020_x_columns)

    def processData(self, data: pd.DataFrame) -> pd.DataFrame:
        # no business logic needed
        return data

    def writeDataToResults(self, data: pd.DataFrame) -> None:
        writeDataFrameToCSV(f"{self.GIT_ROOT}/{DEMOGRAPHICS_RESULTS_FILE_PATH}/population_trends_by_county.csv", data)
