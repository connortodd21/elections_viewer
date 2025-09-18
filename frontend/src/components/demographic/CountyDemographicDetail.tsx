'use client';

import { useState, memo, useEffect } from 'react';
import { County } from '@/interfaces/county';
import { getCountyAgeGroupTrendData, getCountyDemographicTrendData } from '@/api/demographics';
import { getCountyPopulationTrendData } from '@/api/population';
import { DemographicData } from '@/interfaces/demographic';
import { PopulationData } from '@/interfaces/population';
import PopulationCountyChart from './PopulationCountyChart';
import DemographicCountyChart from './DemographicCountyChart';
import { AgeGroupData } from '@/interfaces/age';
import AgeGroupsCountyChart from './AgeGroupCountyChart';

interface CountyDemographicDetailProps {
    detailedCountyData: County;
}

const CountyDemographicDetail = (props: CountyDemographicDetailProps) => {

    const [demographicResults, setDemographicResults] = useState<DemographicData[]>([]);
    const [populationResults, setPopulationResults] = useState<PopulationData[]>([]);
    const [ageGroupResults, setAgeGroupResults] = useState<AgeGroupData[]>([]);

    // TODO: can we parallelize? 
    const { data: demographicData, isPending: isDemographicPending } = getCountyDemographicTrendData(props.detailedCountyData.fips)
    const { data: populationData, isPending: isPopulationPending } = getCountyPopulationTrendData(props.detailedCountyData.fips)
    const { data: ageGroupData, isPending: isAgeGroupPending } = getCountyAgeGroupTrendData(props.detailedCountyData.fips)

    // Update demographic results when new data arrives
	useEffect(() => {
		if (!isDemographicPending && demographicData?.length) {
			setDemographicResults(demographicData);
		}
	}, [demographicData, isDemographicPending]);

    // Update population result when new data arrives
    useEffect(() => {
        if (!isPopulationPending && populationData?.length) {
            setPopulationResults(populationData);
        }
    }, [populationData, isPopulationPending]);

    // Update age result when new data arrives
    useEffect(() => {
        if (!isAgeGroupPending && ageGroupData?.length) {
            setAgeGroupResults(ageGroupData);
        }
    }, [ageGroupData, isAgeGroupPending]);

    if (isDemographicPending && !demographicData) return <div>Loading results...</div>;
    if (isPopulationPending && !populationData) return <div>Loading results...</div>;
    if (isAgeGroupPending && !ageGroupData) return <div>Loading results...</div>;

    return (
        <div className="space-y-8">
            {/* Population Trends */}
            {populationResults.length > 0 && (
                <PopulationCountyChart populationResults={populationResults} />
            )}

            {demographicResults.length > 0 && (
                <DemographicCountyChart demographicResults={demographicResults} />
            )}

            {ageGroupResults.length > 0 && (
                <AgeGroupsCountyChart ageGroupData={ageGroupResults} />
            )}
        </div>
    )
}

export default memo(CountyDemographicDetail);