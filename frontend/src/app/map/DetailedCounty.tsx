import { Button, DialogPanel,  } from '@headlessui/react'
import { useState, memo, useEffect } from 'react'
import type { DSVRowString } from 'd3-dsv';

interface DetailedCountyProps {
  setIsDetailedCountyOpen: React.Dispatch<React.SetStateAction<boolean>>;
  countyName: string
}

const DetailedCounty = (props : DetailedCountyProps) => {

    const [countyResults, setCountyResults] = useState<DSVRowString<string>[]>([]); 

    const getCountyData = async(county: string) => {
        const response = await fetch(`http://localhost:5000/api/get_election_results_for_county/` + county)
        setCountyResults(await response.json())
    }

    useEffect(() => { 
        getCountyData(props.countyName)
    }, []);

    return (
        <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4">
            <DialogPanel
                transition
            >
                <p className="mt-2 text-sm/6 text-white/50">
                Hi
                </p>
                <div className="mt-4">
                <Button
                    onClick={() => {
                        props.setIsDetailedCountyOpen(false)
                    }}
                >
                    Close
                </Button>
                </div>
            </DialogPanel>
            </div>
        </div>
    )
}

export default memo(DetailedCounty);
