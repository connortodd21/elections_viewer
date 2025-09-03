'use client';

import { useState, memo, useEffect } from 'react'

import { getCountyElectionResultsForYear } from '@/api/electionResults';

export interface CountyResult {
    year: string,
    election: string,
    county: string,
    raw_votes_D: string,
    raw_votes_R: string,
    d_candidate: string,
    r_candidate: string
}

interface DetailedElectionResultProps {
    electionYear: string;
    county: string;
    fips: string
}

const D = "D"
const R = "R"

const DetailedElectionResult = (props : DetailedElectionResultProps) => {

    const [countyResultsForYear, setCountyResults] = useState<CountyResult>({
        year: "", election: "", county: "", raw_votes_D: "", raw_votes_R: "", d_candidate: "", r_candidate: ""
    }); 
    
    const { data, isPending, isFetching } = getCountyElectionResultsForYear(
        props.county, props.fips, props.electionYear
    );

    useEffect(() => {
        console.log("DetailedElectionResult useEffect")
        if (!isPending && !isFetching && data) {
            console.log(data)
            setCountyResults(data[0]);
        }
    }, [data, isPending, isFetching, props.electionYear]);

    if (isPending || isFetching) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <div style={{ color: 'green', fontWeight: 'bold'}}>
                {props.electionYear}
            </div>
            <div style={{ color: 'blue', fontWeight: 'bold' }}> 
                {countyResultsForYear.d_candidate} {" "} {countyResultsForYear.raw_votes_D}
            </div>
            <div style={{ color: 'red', fontWeight: 'bold' }}>
                {countyResultsForYear.r_candidate} {" "} {countyResultsForYear.raw_votes_R}
            </div>
        </div>
    )
}

export default memo(DetailedElectionResult);
