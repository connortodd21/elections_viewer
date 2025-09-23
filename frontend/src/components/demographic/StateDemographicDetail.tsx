'use client';

import { useState, useEffect } from 'react';
import { getStateAgeGroupTrendData, getStateDemographicTrendData } from '@/api/demographics';
import { getStatePopulationTrendData } from '@/api/population';
import { DemographicData } from '@/interfaces/demographic';
import { PopulationData } from '@/interfaces/population';
import PopulationCountyChart from './PopulationChart';
import DemographicCountyChart from './DemographicChart';
import { AgeGroupData } from '@/interfaces/age';
import AgeGroupsCountyChart from './AgeGroupChart';

interface StateDemographicDetailProps {
    stateName: string;
}

const StateDemographicDetail = (props: StateDemographicDetailProps) => {

    const [demographicResults, setDemographicResults] = useState<DemographicData[]>([]);
    const [populationResults, setPopulationResults] = useState<PopulationData[]>([]);
    const [ageGroupResults, setAgeGroupResults] = useState<AgeGroupData[]>([]);

    // TODO: can we parallelize? 
    const { data: demographicData, isPending: isDemographicPending } = getStateDemographicTrendData(props.stateName)
    const { data: populationData, isPending: isPopulationPending } = getStatePopulationTrendData(props.stateName)
    const { data: ageGroupData, isPending: isAgeGroupPending } = getStateAgeGroupTrendData(props.stateName)

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

export default StateDemographicDetail;