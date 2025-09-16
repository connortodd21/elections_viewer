import pandas as pd

from common.defs import *
from common.csv_helpers import readCsv, writeDataFrameToCSV
from data_processors.data_processor import DataProcessor

# Raw data file paths
DEMOGRAPHICS_2010_TO_2020_FILE_NAME = "CC-EST2020-ALLDATA-{}"
DEMOGRAPHICS_2021_TO_2024_FILE_NAME = "cc-est2024-alldata-{}"

# Raw data column names
STATE_RAW = "STATE"
COUNTY_RAW = "COUNTY"
YEAR_RAW = "YEAR"
YEAR_RAW_1 = "YEAR_1"
YEAR_RAW_2 = "YEAR_2"
AGEGRP_RAW = "AGEGRP"
SUMLEV_RAW = "SUMLEV"
CTYNAME_RAW = "CTYNAME"
STNAME_RAW = "STNAME"
FIPS_RAW = "FIPS"
YEAR_RAW = "YEAR"
AGEGRP_RAW = "AGEGRP"
TOT_POP_RAW = "TOT_POP"
TOT_MALE_RAW = "TOT_MALE"
TOT_FEMALE_RAW = "TOT_FEMALE"
WA_MALE_RAW = "WA_MALE"
WA_FEMALE_RAW = "WA_FEMALE"
BA_MALE_RAW = "BA_MALE"
BA_FEMALE_RAW = "BA_FEMALE"
IA_MALE_RAW = "IA_MALE"
IA_FEMALE_RAW = "IA_FEMALE"
AA_MALE_RAW = "AA_MALE"
AA_FEMALE_RAW = "AA_FEMALE"
NA_MALE_RAW = "NA_MALE"
NA_FEMALE_RAW = "NA_FEMALE"
TOM_MALE_RAW = "TOM_MALE"
TOM_FEMALE_RAW = "TOM_FEMALE"
WAC_MALE_RAW = "WAC_MALE"
WAC_FEMALE_RAW = "WAC_FEMALE"
BAC_MALE_RAW = "BAC_MALE"
BAC_FEMALE_RAW = "BAC_FEMALE"
IAC_MALE_RAW = "IAC_MALE"
IAC_FEMALE_RAW = "IAC_FEMALE"
AAC_MALE_RAW = "AAC_MALE"
AAC_FEMALE_RAW = "AAC_FEMALE"
NAC_MALE_RAW = "NAC_MALE"
NAC_FEMALE_RAW = "NAC_FEMALE"
H_MALE_RAW = "H_MALE"
H_FEMALE_RAW = "H_FEMALE"

# output data columns
HISPANIC_MALE = "HISPANIC_MALE"
HISPANIC_FEMALE = "HISPANIC_FEMALE"

ZERO = "0"
MINUS_1 = "-1"

class DemographicTrendsByCounty(DataProcessor):

    def __init__(self, state: str) -> None:
        self.intermediate_file_path = f"{self.GIT_ROOT}/{DEMOGRAPHICS_INTERMIEDIATE_FILE_PATH}/intermediate_results.csv"
        super().__init__(state)

    def getRawData(self) -> pd.DataFrame:
        # census data is divided into pre 2010-2020 and 2020-2024 datasets. need to read from both and concat
        encoding = "latin1" # needed to avoid encoding error when reading csv
        converters = {STATE_RAW: str, COUNTY_RAW: str, YEAR_RAW: str, AGEGRP_RAW: str}
        census_2010_to_2020_data = readCsv(f"{self.GIT_ROOT}/{DEMOGRAPHICS_RAW_FILE_PATH}/{DEMOGRAPHICS_2010_TO_2020_FILE_NAME.format(STATE_TO_FIPS[self.state])}.csv",encoding=encoding,converters=converters)
        census_2020_to_2024_data = readCsv(f"{self.GIT_ROOT}/{DEMOGRAPHICS_RAW_FILE_PATH}/{DEMOGRAPHICS_2021_TO_2024_FILE_NAME.format(STATE_TO_FIPS[self.state])}.csv",encoding=encoding,converters=converters)
        # the year columns use repeat values to represent years. In 2010 dataset 1 = 2010 andin 2020 dataset 1 = 2020
        # need to handle these separately, so splitting into two columns for now. the other columns can be merged
        census_2010_to_2020_data = census_2010_to_2020_data.rename(columns={YEAR_RAW: YEAR_RAW_1})
        census_2020_to_2024_data = census_2020_to_2024_data.rename(columns={YEAR_RAW: YEAR_RAW_2})
        data = pd.concat([census_2010_to_2020_data, census_2020_to_2024_data], ignore_index=True)
        data = data.fillna({YEAR_RAW_1: ZERO, YEAR_RAW_2: ZERO})
        return data

    def filterData(self, data: pd.DataFrame) -> pd.DataFrame:

        # during data cleaning, we assigned values of -1 for features we didnt want (year, age group)
        # here we will remove the rwos with those values
        def filter_rows_with_negative_1(data: pd.DataFrame) -> pd.DataFrame:
            return data[(data[AGEGRP_RAW] != MINUS_1) & (data[YEAR_RAW] != MINUS_1)]

        # we only care about data after 2016
        def filter_pre_2016_years(data: pd.DataFrame) -> pd.DataFrame:
            return data[data[YEAR_RAW] >= "2016"]

        return data.pipe(filter_rows_with_negative_1).pipe(filter_pre_2016_years)

    def cleanData(self, data: pd.DataFrame) -> pd.DataFrame:

        # make column names more descriptive/clear
        def rename_columns(data: pd.DataFrame) -> pd.DataFrame:
            # keys are raw data prefixes. values is the prefixes we will rename to 
            prefix_map = {
                "WA": "WHITE",
                "BA": "BLACK",
                "IA": "INDIAN",
                "AA": "ASIAN",
                "NA": "NATIVE",
                "TOM": "TWO_OR_MORE",
                "WAC": "WHITE_COMBINATION",
                "BAC": "BLACK_COMBINATION",
                "IAC": "INDIAN_COMBINATION",
                "AAC": "ASIAN_COMBINATION",
                "NAC": "NATIVE_COMBINATION",
                "H": "HISPANIC",
            }
            renamed_columns = {}
            columns = list(data.columns)
            for col in columns:
                for prefix, full in prefix_map.items():
                    if col.startswith(prefix + "_"):
                        renamed_columns[col] = col.replace(prefix, full, 1)

            data = data.rename(columns=renamed_columns)
            return data

        # years are represented as integers. convert those integers into real years
        def standardize_years(data: pd.DataFrame) -> pd.DataFrame:
            # replace values from the 2010-2020 dataset
            year1_values_to_years = {
                "1": "2010",
                "2": MINUS_1,  # we will remove this row later. it is an estimate. 1 is the real data
                "3": MINUS_1,  # we will remove this row later. it is an estimate for july. 1 is the real data in april
                "4": "2011", "5": "2012", "6": "2013", "7": "2014", "8": "2015", "9": "2016", "10": "2017", "11": "2018", "12": "2019",
                "13": MINUS_1,  # we will remove this row later. it is an estimate for april. 14 is the estimate for july. we will use that
                "14": MINUS_1  # This is the 2020 data. we will use the 2020 data from the 2020-2024 dataset instead
            }
            data[YEAR_RAW_1] = data[YEAR_RAW_1].replace(year1_values_to_years)

            # replace values from the 2020-2024 dataset
            year2_values_to_years = {
                "1": MINUS_1,  # we will remove this row later. it is an estimate for april. 2 is the estimate for july. we will use that
                "2": "2020", "3": "2021", "4": "2022", "5": "2023", "6": "2024"
            }
            data[YEAR_RAW_2] = data[YEAR_RAW_2].replace(year2_values_to_years)

            # merge year1 and year2 vertically
            data[YEAR_RAW] = data[YEAR_RAW_1].mask(data[YEAR_RAW_1] == ZERO, data[YEAR_RAW_2])

            self.move_column_to_left(data, YEAR_RAW)
            return data

        # combine state + county fips into one code
        def combine_fips(data: pd.DataFrame) -> pd.DataFrame:
            data[FIPS] = data[STATE_RAW].str.pad(width=2, side='left', fillchar='0') + data[COUNTY_RAW].str.pad(width=3, side='left', fillchar='0')
            # move to left of dataframe
            self.move_column_to_left(data, FIPS)
            return data

        # age groups are represented as integers. convert those integers into real ranges
        def standardize_age_groups(data: pd.DataFrame) -> pd.DataFrame:
            age_group_values_to_ages = {
                "0": MINUS_1, # total for all groups
                "1": MINUS_1, "2": MINUS_1, "3": MINUS_1, "4": MINUS_1, # contain below voting age ages
                "5": "20-24", "6": "25-29", "7": "30-34", "8": "35-39", "9": "40-44", "10": "45-49",
                "11": "50-54", "12": "55-59", "13": "60-64", "14": "65-69", "15": "70-74", "16": "75-79",
                "17": "80-84", "18": "85+"
            }
            data[AGEGRP_RAW] = data[AGEGRP_RAW].replace(age_group_values_to_ages)
            return data

        return data.pipe(standardize_years).pipe(combine_fips).pipe(standardize_age_groups).pipe(rename_columns)

    def dropData(self, data: pd.DataFrame) -> pd.DataFrame:

        # might revist these, but mostly focused on demographic trends right now so dont need these columns
        def drop_hispanic_identifying_columns(data: pd.DataFrame) -> pd.DataFrame:
            hispanic_prefix = "H"
            non_hispanic_prefix = "NH"
            drop_columns = []
            columns = list(data.columns)
            for column in columns:
                if (column != HISPANIC_MALE and column != HISPANIC_FEMALE) and (column[0] == hispanic_prefix or column[0:2] == non_hispanic_prefix):
                    drop_columns.append(column)
            return data.drop(drop_columns, axis=1) 

        # these are artifacts of the data pre-merging. we can safely drop
        def drop_original_year_columns(data: pd.DataFrame) -> pd.DataFrame:
            return data.drop([YEAR_RAW_1, YEAR_RAW_2], axis=1)       

        # these columns are unnecessary
        def drop_unnecessary_descriptors(data: pd.DataFrame) -> pd.DataFrame:
            drop_columns = [STATE_RAW, COUNTY_RAW, SUMLEV_RAW, CTYNAME_RAW, STNAME_RAW]
            return data.drop(drop_columns, axis=1) 

        return data.pipe(drop_original_year_columns).pipe(drop_unnecessary_descriptors).pipe(drop_hispanic_identifying_columns)

    def processData(self, data: pd.DataFrame) -> pd.DataFrame:
        # no business logic needed
        return data

    def writeDataToResults(self, data: pd.DataFrame) -> None:
        writeDataFrameToCSV(f"{self.GIT_ROOT}/{DEMOGRAPHICS_RESULTS_FILE_PATH}/demographic_trends_by_county.csv", data)

    ################################################################################
    #### Custom functions for this class
    ################################################################################

    # move a column to the 0 index (left side) of dataframe
    def move_column_to_left(self, data: pd.DataFrame, column_name: str) -> pd.DataFrame:
        column_to_move = data.pop(column_name)
        data.insert(0, column_name, column_to_move) # Insert it at index 0
        return data