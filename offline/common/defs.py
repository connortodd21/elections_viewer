# database paths
PROCESSED_DATA_FILE_PATH = "database/{}/processed"
RAW_DATA_FILE_PATH = "database/{}/raw"
RESULTS_FILE_PATH = "database/{}/results"
COUNTIES_FILE_PATH = "database/{}/counties"
ALL_COUNTIES_FILE_PATH = "database/counties"
DEMOGRAPHICS_FILE_PATH = "database/demographics"

# years since trump entered politics
ELECTION_YEARS_AFTER_TRUMP = [2016, 2018, 2020, 2022, 2024]

# common strings
PRESIDENT = "president"
SENATE = "senate"
GOVERNOR = "governor"

# all-counties-related keys
NAME = "Name"
STATE = "State"
FIPS = "FIPS"

# Demographics constants
AGE_SEX_RACE = "AgeSexRace"

# Individual va
AL = "AL"
AK = "AK"
AZ = "AZ"
AR = "AR"
CA = "CA"
CO = "CO"
CT = "CT"
DE = "DE"
DC = "DC"
FL = "FL"
GA = "GA"
HI = "HI"
ID = "ID"
IL = "IL"
IN = "IN"
IA = "IA"
KS = "KS"
KY = "KY"
LA = "LA"
ME = "ME"
MD = "MD"
MA = "MA"
MI = "MI"
MN = "MN"
MS = "MS"
MO = "MO"
MT = "MT"
NE = "NE"
NV = "NV"
NH = "NH"
NJ = "NJ"
NM = "NM"
NY = "NY"
NC = "NC"
ND = "ND"
OH = "OH"
OK = "OK"
OR = "OR"
PA = "PA"
RI = "RI"
SC = "SC"
SD = "SD"
TN = "TN"
TX = "TX"
UT = "UT"
VT = "VT"
VA = "VA"
WA = "WA"
WV = "WV"
WI = "WI"
WY = "WY"

# States and their two letter abbreviation
VALID_US_STATES = set([
    AL, AK, AZ, AR, CA, CO, CT, DC, DE, FL, GA,
    HI, ID, IL, IN, IA, KS, KY, LA, ME, MD,
    MA, MI, MN, MS, MO, MT, NE, NV, NH, NJ,
    NM, NY, NC, ND, OH, OK, OR, PA, RI, SC,
    SD, TN, TX, UT, VT, VA, WA, WV, WI, WY
])

US_STATES_FULL_NAMES = set(
    ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"]
)