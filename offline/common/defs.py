# database paths
PROCESSED_DATA_FILE_PATH = "database/{}/processed"
RAW_DATA_FILE_PATH = "database/{}/raw"
RESULTS_FILE_PATH = "database/{}/results"
COUNTIES_FILE_PATH = "database/{}/counties"
ALL_COUNTIES_FILE_PATH = "database/counties"
DEMOGRAPHICS_RAW_FILE_PATH = "database/demographics/raw"
DEMOGRAPHICS_INTERMIEDIATE_FILE_PATH = "database/demographics/intermediate"
DEMOGRAPHICS_RESULTS_FILE_PATH = "database/demographics/results"

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

# County results column names
YEAR = "year"
ELECTION = "election"
COUNTY = "county"
RAW_VOTES_D = "raw_votes_D"
RAW_VOTES_R = "raw_votes_R"
D_CANDIDATE = "d_candidate"
R_CANDIDATE = "r_candidate"

# Demographics constants
POPULATION_TRENDS_BY_COUNTY = "PopulationTrendsByCounty"
DEMOGRAPHIC_TRENDS_BY_COUNTY = "DemographicTrendsByCounty"

# Individual state abbreviations
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

STATE_TO_FIPS = {
    AL: "01",
    AK: "02",
    AZ: "04",
    AR: "05",
    CA: "06",
    CO: "08",
    CT: "09",
    DE: "10",
    FL: "12",
    GA: "13",
    HI: "15",
    ID: "16",
    IL: "17",
    IN: "18",
    IA: "19",
    KS: "20",
    KY: "21",
    LA: "22",
    ME: "23",
    MD: "24",
    MA: "25",
    MI: "26",
    MN: "27",
    MS: "28",
    MO: "29",
    MT: "30",
    NE: "31",
    NV: "32",
    NH: "33",
    NJ: "34",
    NM: "35",
    NY: "36",
    NC: "37",
    ND: "38",
    OH: "39",
    OK: "40",
    OR: "41",
    PA: "42",
    RI: "44",
    SC: "45",
    SD: "46",
    TN: "47",
    TX: "48",
    UT: "49",
    VT: "50",
    VA: "51",
    WA: "53",
    WV: "54",
    WI: "55",
    WY: "56"
}
