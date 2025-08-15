import pandas as pd

# write DF to csv
def writeDataFrameToCSV(path: str, data: pd.DataFrame) -> None: 
    open(path, 'w').close()
    data.to_csv(path,  index=False)

# read csv as Df
def readData(path: str) -> pd.DataFrame:
    return pd.read_csv(path,  sep='\t', index_col=None, lineterminator="\n")
    