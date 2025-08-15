import pandas as pd

from common.defs import *

# the office codes are different for senate in 2024 than previous years
def getCorrectOfficeCodes(year: str) -> dict:
    return OFFICE_CODES_NEW if year == "2024" else OFFICE_CODES_OLD

    