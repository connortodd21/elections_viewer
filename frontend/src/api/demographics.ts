import axios from 'axios';
import { useQuery } from '@tanstack/react-query'
import { DemographicData } from '@/interfaces/demographic';
import { AgeGroupData } from '@/interfaces/age';

const HEADER = "http://127.0.0.1:5000/api/"
const DEMOGRAPHIC_TRENDS_FOR_COUNTY = HEADER + "get_demographic_trends_for_county"
const DEMOGRAPHIC_TRENDS_FOR_STATE = HEADER + "get_demographic_trends_for_state"
const AGE_TRENDS_FOR_COUNTY = HEADER + "get_age_trends_for_county"
const AGE_TRENDS_FOR_STATE = HEADER + "get_age_trends_for_state"


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

/**
 * Get age trend for county
 */
const fetchCountyAgeGroupTrendData = async (fips: string): Promise<Array<AgeGroupData>> => {
        const response = await axios.get(`${AGE_TRENDS_FOR_COUNTY}/${fips}`)
        return await response.data
    }

const getCountyAgeGroupTrendData = (fips: string) => {
    return useQuery({
        queryKey: ['get_age_group_trends_for_county', fips],
        queryFn: () => fetchCountyAgeGroupTrendData(fips)
    })
}

/**
 * Get age trend for state
 */
const fetchStateAgeGroupTrendData = async (state: string): Promise<Array<AgeGroupData>> => {
        const response = await axios.get(`${AGE_TRENDS_FOR_STATE}/${state}`)
        return await response.data
    }

const getStateAgeGroupTrendData = (state: string) => {
    return useQuery({
        queryKey: ['get_age_group_trends_for_state', state],
        queryFn: () => fetchStateAgeGroupTrendData(state)
    })
}

export { getCountyDemographicTrendData, getStateDemographicTrendData, getCountyAgeGroupTrendData, getStateAgeGroupTrendData }