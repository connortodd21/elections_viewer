import { Button, DialogPanel,  } from '@headlessui/react'
import { useState, memo, useEffect } from 'react'
import type { DSVRowString } from 'd3-dsv';

import { CountyData } from './MapChart';

interface CountyResults {
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

    const [countyResults, setCountyResults] = useState<CountyResults[]>([]); 

    const getCountyData = async(county: string, fips: string) => {
        const response = await fetch(`http://localhost:5000/api/get_election_results_for_county/` + fips + "/" + county)
        setCountyResults(await response.json())
    }

    useEffect(() => { 
        getCountyData(props.detailedCountyData.countyName, props.detailedCountyData.fips)
    }, []);

    return (
        <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4">
            <DialogPanel
                transition
            >
                <p style={{ color: 'purple', fontWeight: 'bold' }}>{props.detailedCountyData.countyName}</p> 
                <ul>
                    {countyResults.map((countyResult) => (
                        <div>
                            <li key={countyResult.year+"_"+countyResult.election} style={{ color: 'green', fontWeight: 'bold' }}>
                                {countyResult.d_candidate} {countyResult.raw_votes_D} {" "}       
                                {countyResult.r_candidate} {countyResult.raw_votes_R}
                            </li>
                        </div>
                    ))}
                </ul>
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
