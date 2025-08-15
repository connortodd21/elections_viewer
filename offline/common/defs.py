# column names used in raw datasets
PARTY_DESCRIPTION = "PartyDescription"
PARTY_NAMES = ["Democratic", "Republican", "DEMOCRATIC", "REPUBLICAN"]
REPUBLICAN = ["Republican", "REPUBLICAN"]
DEMOCRAT = ["Democratic", "DEMOCRATIC"]
COUNTY_NAME = "CountyName"
CANDIDATE_VOTES = "CandidateVotes"
OFFICE_CODE = "OfficeCode(text)"
# office code mappings in raw datasets from 2016-2022
OFFICE_CODES_OLD = {
    "1": "president",
    "2": "governor",
    "5": "senate"
}
# office code mappings in raw datasets in 2024
OFFICE_CODES_NEW = {
    "1": "president",
    "2": "governor",
    "7": "senate"
}

# general macros
COUNTY = "county"
CANDIDATE_FULL_NAME = "CandidateFullName"

# columns for county_by_county_results in parse_results.py
YEAR = "year"
ELECTION = "election"
RAW_VOTES_D = "raw_votes_D"
RAW_VOTES_R = "raw_votes_R"
D_CANDIDATE = "d_candidate"
R_CANDIDATE = "r_candidate"

# database paths
PROCESSED_DATA_FILE_PATH = "database/{}/processed"
RAW_DATA_FILE_PATH = "database/{}/raw"
RESULTS_FILE_PATH = "database//results"
MI_RAW_DATA_FILE_NAME = "STATE_GENERAL_MI_CENR_BY_COUNTY"
