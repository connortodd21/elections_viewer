import axios from 'axios';
import { useQuery } from '@tanstack/react-query'

import { CountyResult } from '@/components/DetailedElectionResult';

const HEADER = "http://127.0.0.1:5000/api/"
const RESULTS_ENDPOINT = HEADER + "get_election_results_for_county/"
const RESULTS_FOR_YEAR_ENDPOINT = HEADER + "get_election_results_for_county_and_year"

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

const fetchElectionResultsForYear = async (countyName: string, fips: string, year: string): Promise<Array<CountyResult>> => {
        const response = await axios.get(`${RESULTS_FOR_YEAR_ENDPOINT}/${fips}/${countyName}/${year}`)
        return await response.data
    }

const getCountyElectionResultsForYear = (countyName: string, fips: string, year: string) => {
    return useQuery({
        queryKey: ['getCountyElectionResultsForYear', fips],
        queryFn: () => fetchElectionResultsForYear(countyName, fips, year)
    })
}

export { getCountyElectionResults, getCountyElectionResultsForYear }