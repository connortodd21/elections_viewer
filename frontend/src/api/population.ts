import axios from 'axios';
import { useQuery } from '@tanstack/react-query'
import { PopulationData } from '@/interfaces/population';

const HEADER = "http://127.0.0.1:5000/api/"
const POPULATION_TRENDS_FOR_COUNTY = HEADER + "get_population_trends_for_county"
const POPULATION_TRENDS_FOR_STATE = HEADER + "get_population_trends_for_state"

/**
 * Get population trend data for a county
 */
const fetchCountyPopulationTrendData = async (fips: string): Promise<Array<PopulationData>> => {
        const response = await axios.get(`${POPULATION_TRENDS_FOR_COUNTY}/${fips}`)
        return await response.data
    }

const getCountyPopulationTrendData = (fips: string) => {
    return useQuery({
        queryKey: ['get_population_trends_for_county', fips],
        queryFn: () => fetchCountyPopulationTrendData(fips)
    })
}

/**
 * Get population trend data for a state
 */
const fetchStatePopulationTrendData = async (state: string): Promise<Array<PopulationData>> => {
        const response = await axios.get(`${POPULATION_TRENDS_FOR_STATE}/${state}`)
        return await response.data
    }

const getStatePopulationTrendData = (state: string) => {
    return useQuery({
        queryKey: ['get_population_trends_for_state', state],
        queryFn: () => fetchStatePopulationTrendData(state)
    })
}


export { getCountyPopulationTrendData, getStatePopulationTrendData }