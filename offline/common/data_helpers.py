import pandas as pd

from common.defs import *

def generateCountyFipsRow(name: str, state: str, fips: str) -> pd.DataFrame:
    return pd.DataFrame({
        NAME: [name],
        STATE: [state],
        FIPS: [fips]
    })