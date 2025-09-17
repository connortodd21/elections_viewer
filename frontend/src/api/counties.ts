import axios from 'axios';
import { useQuery } from '@tanstack/react-query'
import { County, CountyResult } from '@/interfaces/county';


const HEADER = "http://127.0.0.1:5000/api/"
const RESULTS_ENDPOINT = HEADER + "get_election_results_for_county"
const RESULTS_FOR_YEAR_ENDPOINT = HEADER + "get_election_results_for_county_and_year"
const SWING_COUNTIES_ENDPOINT = HEADER + "get_swing_counties"
const ELECTION_YEARS_ENDPOINT = HEADER + "get_county_election_years"


/**
 * Get recent election results for a county
 */
const fetchElectionResults = async (countyName: string, fips: string): Promise<Array<CountyResult>> => {
        const response = await axios.get(`${RESULTS_ENDPOINT}/${fips}/${countyName}`)
        return await response.data
    }

const getCountyElectionResults = (countyName: string, fips: string) => {
    return useQuery({
        queryKey: ['getCountyElectionResults', fips],
        queryFn: () => fetchElectionResults(countyName, fips)
    })
}

/**
 * Get election results for a county for a specific year
 */
const fetchElectionResultsForYear = async (countyName: string, fips: string, year: string): Promise<Array<CountyResult>> => {
        const response = await axios.get(`${RESULTS_FOR_YEAR_ENDPOINT}/${fips}/${countyName}/${year}`)
        return await response.data
    }

const getCountyElectionResultsForYear = (countyName: string, fips: string, year: string) => {
    return useQuery({
        queryKey: ['getCountyElectionResultsForYear', fips, year],
        queryFn: () => fetchElectionResultsForYear(countyName, fips, year)
    })
}

/**
 * Get swing counties for a state
 */
const fetchSwingCounties = async (state: string): Promise<Array<County>> => {
        const response = await axios.get(`${SWING_COUNTIES_ENDPOINT}/${state}`)
        return await response.data
    }

const getSwingCounties = (state?: string | null) => {
    return useQuery({
        queryKey: ['getSwingCounties', state],
        queryFn: () => fetchSwingCounties(state as string),
        enabled: !!state && false, // don't auto-run, must be refetched
    })
}

/**
 * Get statewide election years for a county
 */
const fetchElectionYears = async (countyName: string, fips: string): Promise<Array<string>> => {
        const response = await axios.get(`${ELECTION_YEARS_ENDPOINT}/${fips}/${countyName}`)
        return await response.data
    }

const getCountyElectionYears = (countyName: string, fips: string) => {
    return useQuery({
        queryKey: ['getCountyElectionData', fips],
        queryFn: () => fetchElectionYears(countyName, fips)
    })
}

export { getCountyElectionResults, getCountyElectionResultsForYear, getSwingCounties, getCountyElectionYears }