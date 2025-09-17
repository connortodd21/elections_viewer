import axios from 'axios';
import { useQuery } from '@tanstack/react-query'
import { StateResult } from '@/interfaces/state';

const HEADER = "http://127.0.0.1:5000/api/"
const RESULTS_ENDPOINT = HEADER + "get_election_results_for_state"
const RESULTS_FOR_YEAR_ENDPOINT = HEADER + "get_election_results_for_state_and_year"

/**
 * Get recent election results for a state
 */
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

/**
 * Get election results for a state in a specific year
 */
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