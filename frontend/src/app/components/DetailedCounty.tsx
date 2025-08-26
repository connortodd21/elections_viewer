import { Button, DialogPanel, DialogBackdrop } from '@headlessui/react'
import { useState, memo, useEffect } from 'react'

import { CountyData } from './MapChart';
import ElectionResult from './DetailedElectionResult';

export interface CountyResult {
    year: string,
    election: string,
    county: string,
    raw_votes_D: string,
    raw_votes_R: string,
    d_candidate: string,
    r_candidate: string
}

interface DetailedCountyProps {
  setIsDetailedCountyOpen: React.Dispatch<React.SetStateAction<boolean>>;
  detailedCountyData: CountyData
}

const DetailedCounty = (props : DetailedCountyProps) => {
    
    const [countyResults, setCountyResults] = useState<CountyResult[]>([]); 
    const [electionYears, setElectionYears] = useState<String[]>([])

    const getCountyData = async(county: string, fips: string) => {
        const response = await fetch(`http://localhost:5000/api/get_election_results_for_county/` + fips + "/" + county)
        let results = await response.json()
        setCountyResults(results)
        setElectionYears([...new Set<String>(results.map((item: CountyResult) => item.year))]);
    }

    useEffect(() => { 
        getCountyData(props.detailedCountyData.countyName, props.detailedCountyData.fips)
    }, []);

    return (
        <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4">
                <DialogPanel transition autoFocus
                    className="w-full max-w-md rounded-xl bg-white/5 p-6 backdrop-blur-2xl duration-300 ease-out data-closed:transform-[scale(95%)] data-closed:opacity-0"
                >
                    <DialogBackdrop className="fixed inset-0 bg-black/30" />
                    <p style={{ color: 'purple', fontWeight: 'bold' }}>{props.detailedCountyData.countyName}</p> 
                    {countyResults.map((countyResult) => (
                        <ElectionResult electionResult={countyResult} ></ElectionResult>
                    ))}
                    <Button
                        style={{ color: 'red', fontWeight: 'bold' }}
                        onClick={() => {
                            props.setIsDetailedCountyOpen(false)
                        }}
                    >
                        Close
                    </Button>
                </DialogPanel>
            </div>
        </div>
    )
}

export default memo(DetailedCounty);
