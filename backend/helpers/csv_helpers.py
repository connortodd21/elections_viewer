import pandas as pd

# read csv as Df with more customization
def readCsv(path: str, names=None, skiprows=0, thousands=None, converters=None) -> pd.DataFrame:
    return pd.read_csv(path, index_col=None, names=names, skiprows=skiprows, thousands=thousands, converters=converters)
    