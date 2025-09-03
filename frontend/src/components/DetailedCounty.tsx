import { DialogPanel, DialogBackdrop } from '@headlessui/react'
import { useState, memo, useEffect } from 'react'
import Select, {SingleValue, ActionMeta} from 'react-select';

import { CountyData } from './map/Map';
import DetailedElectionResult from './DetailedElectionResult';
import { getCountyElectionYears } from '@/api/counties'; 


interface DetailedCountyProps {
  closeDialog: () => void ;
  detailedCountyData: CountyData
}

interface SelectOptionType {
  value: string;
  label: string;
}

const DetailedCounty = (props : DetailedCountyProps) => {
    
    const [electionYears, setElectionYears] = useState<string[]>([])
    const [selectedElectionYear, setSelectedElectionYear] = useState("")

    const { data, isPending, isFetching } = getCountyElectionYears(
        props.detailedCountyData.countyName,
        props.detailedCountyData.fips
    );

    const handleSelectChange = (newValue: SingleValue<SelectOptionType>, actionMeta: ActionMeta<SelectOptionType>) => {
        console.log(newValue)
        setSelectedElectionYear(newValue?.value ?? "");
    };

    useEffect(() => {
        if (!isPending && !isFetching && data) {
            setElectionYears(data);
            setSelectedElectionYear(data[0])
        }
    }, [data, isPending, isFetching]);

    const options: SelectOptionType[] = electionYears.map(year => ({
        value: year,
        label: year,
    }));

    if (isPending || isFetching) {
        return <div>Loading...</div>;
    }

    return (
        <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4">
                <DialogBackdrop className="fixed inset-0 bg-black/40 backdrop-blur-sm transition-opacity" />
                <div className="fixed inset-0 flex items-center justify-center p-4">
                    <DialogPanel
                        autoFocus
                        className="w-full max-w-md rounded-xl bg-white/80 p-6 shadow-xl ring-1 ring-white/20 backdrop-blur-2xl transition duration-300 ease-out data-closed:transform-[scale(95%)] data-closed:opacity-0"
                    >
                        {/* Dialog content */}
                        <Select<SelectOptionType, false>
                            options={options}
                            defaultValue={options[0]}
                            value={options.find(opt => opt.value === selectedElectionYear) || options[0]}
                            onChange={handleSelectChange}
                            placeholder="Choose Year"
                            styles={{
                                option: (provided) => ({
                                    ...provided,
                                    color: "#111", // darker text for dropdown options
                                }),
                                singleValue: (provided) => ({
                                    ...provided,
                                    color: "#111", // darker text for selected value
                            }),
                        }}
                        />
                        <p className="text-lg font-bold text-purple-600">
                            {props.detailedCountyData.countyName}
                        </p>

                        <DetailedElectionResult
                            electionYear={selectedElectionYear}
                            county={props.detailedCountyData.countyName}
                            fips={props.detailedCountyData.fips}
                        />

                        <button
                            type="button"
                            className="mt-4 rounded-lg bg-red-600 px-4 py-2 font-bold text-white shadow hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-400"
                            onClick={() => props.closeDialog()}
                        >
                        Close
                        </button>
                    </DialogPanel>
                </div>
            </div>
        </div>
    )
}

export default memo(DetailedCounty);
