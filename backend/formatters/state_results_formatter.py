import pandas as pd

from helpers.constants import *

def format_results_for_state(county_data: pd.DataFrame, state: str) -> pd.DataFrame:
    """
        Given a dataframe with county by county results for a state, return the combined results for the 
        entire state
    """
    statewide_results = pd.DataFrame(columns=[YEAR, ELECTION, STATE, RAW_VOTES_D, RAW_VOTES_R, D_CANDIDATE, R_CANDIDATE])
    results_for_year = [d for _, d in county_data.groupby([YEAR])]
    for result_for_year in results_for_year:
        results_for_election = [d for _, d in result_for_year.groupby([ELECTION])]
        for result_for_election in results_for_election:
            state_results = pd.DataFrame({
                YEAR: [result_for_election[YEAR].unique()[0]],
                ELECTION: [result_for_election[ELECTION].unique()[0]],
                STATE: [state],
                RAW_VOTES_D: [result_for_election[RAW_VOTES_D].sum()],
                RAW_VOTES_R: [result_for_election[RAW_VOTES_R].sum()],
                D_CANDIDATE: [result_for_election[D_CANDIDATE].unique()[0]],
                R_CANDIDATE: [result_for_election[R_CANDIDATE].unique()[0]]
            })
            statewide_results = pd.concat([statewide_results, state_results])
    return statewide_results