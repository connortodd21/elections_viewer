import axios from 'axios';
import { useQuery } from '@tanstack/react-query'

const ENDPOINT = "http://127.0.0.1:5000/api/get_county_election_years"

const fetchElectionYears = async (countyName: string, fips: string): Promise<Array<string>> => {
        const response = await axios.get(`${ENDPOINT}/${fips}/${countyName}`)
        return await response.data
    }

const getCountyElectionYears = (countyName: string, fips: string) => {
    return useQuery({
        queryKey: ['getCountyElectionData', fips],
        queryFn: () => fetchElectionYears(countyName, fips)
    })
}

export { getCountyElectionYears }