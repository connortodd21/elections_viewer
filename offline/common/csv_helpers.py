import pandas as pd

from common.os_helpers import createDirectoryIfNotExists, createFile

# write DF to csv. Creates path and file if either do not exist
def writeDataFrameToCSV(path: str, data: pd.DataFrame) -> None: 
    createDirectoryIfNotExists(path)
    createFile(path)
    data.to_csv(path,  index=False)

# read csv as Df
def readTsvAsCsv(path: str) -> pd.DataFrame:
    return pd.read_csv(path,  sep='\t', index_col=None, lineterminator="\n")

# read csv as Df with more customization
def readCsv(path: str, names=None, skiprows=0, thousands=None) -> pd.DataFrame:
    return pd.read_csv(path, index_col=None, names=names, skiprows=skiprows, thousands=thousands)
    