import pandas as pd

# write DF to csv
def writeDataFrameToCSV(path: str, data: pd.DataFrame) -> None: 
    open(path, 'w').close()
    data.to_csv(path,  index=False)

# read csv as Df
def readTsvAsCsv(path: str) -> pd.DataFrame:
    return pd.read_csv(path,  sep='\t', index_col=None, lineterminator="\n")

def readCsv(path: str, names=None, skiprows=0, thousands=None) -> pd.DataFrame:
    return pd.read_csv(path, index_col=None, names=names, skiprows=skiprows, thousands=thousands)
    