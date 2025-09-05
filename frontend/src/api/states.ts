import axios from 'axios';
import { useQuery } from '@tanstack/react-query'

const HEADER = "http://127.0.0.1:5000/api/"
const RESULTS_ENDPOINT = HEADER + "get_election_results_for_state/"
const RESULTS_FOR_YEAR_ENDPOINT = HEADER + "get_election_results_for_state_and_year"

export interface StateResult {
  year: string;
  election: string;
  state: string;
  raw_votes_D: string;
  raw_votes_R: string;
  d_candidate: string;
  r_candidate: string;
}

// Empty template object
export const emptyStateResult: StateResult = {
  year: "",
  election: "",
  state: "",
  raw_votes_D: "",
  raw_votes_R: "",
  d_candidate: "",
  r_candidate: "",
};

const fetchElectionResults = async (state: string): Promise<Array<StateResult>> => {
        const response = await axios.get(`${RESULTS_ENDPOINT}/${state}`)
        return await response.data
    }

const getStateElectionResults = (state: string) => {
    return useQuery({
        queryKey: ['getStateElectionResults', state],
        queryFn: () => fetchElectionResults(state)
    })
}

const fetchElectionResultsForYear = async (state: string,  year: string): Promise<Array<StateResult>> => {
        const response = await axios.get(`${RESULTS_FOR_YEAR_ENDPOINT}/${state}/${year}`)
        return await response.data
    }

const getStateElectionResultsForYear = (state: string, year: string) => {
    return useQuery({
        queryKey: ['getStateElectionResultsForYear', state, year],
        queryFn: () => fetchElectionResultsForYear(state, year)
    })
}

export { getStateElectionResults, getStateElectionResultsForYear }