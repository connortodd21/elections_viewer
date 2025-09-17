import axios from 'axios';
import { useQuery } from '@tanstack/react-query'
import { DemographicData } from '@/interfaces/demographic';

const HEADER = "http://127.0.0.1:5000/api/"
const DEMOGRAPHIC_TRENDS_FOR_COUNTY = HEADER + "get_demographic_trends_for_county"
const DEMOGRAPHIC_TRENDS_FOR_STATE = HEADER + "get_demographic_trends_for_state"

/**
 * Get demographic trend data for a county
 */
const fetchCountyDemographicTrendData = async (fips: string): Promise<Array<DemographicData>> => {
        const response = await axios.get(`${DEMOGRAPHIC_TRENDS_FOR_COUNTY}/${fips}`)
        return await response.data
    }

const getCountyDemographicTrendData = (fips: string) => {
    return useQuery({
        queryKey: ['get_demographic_trends_for_county', fips],
        queryFn: () => fetchCountyDemographicTrendData(fips)
    })
}

/**
 * Get demographic trend data for a state
 */
const fetchStateDemographicTrendData = async (state: string): Promise<Array<DemographicData>> => {
        const response = await axios.get(`${DEMOGRAPHIC_TRENDS_FOR_STATE}/${state}`)
        return await response.data
    }

const getStateDemographicTrendData = (state: string) => {
    return useQuery({
        queryKey: ['get_demographic_trends_for_state', state],
        queryFn: () => fetchStateDemographicTrendData(state)
    })
}


export { getCountyDemographicTrendData, getStateDemographicTrendData }