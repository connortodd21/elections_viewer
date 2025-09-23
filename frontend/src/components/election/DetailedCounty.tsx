'use client';

import { DialogPanel, DialogBackdrop } from '@headlessui/react';
import { useState, memo, useEffect } from 'react';

import DetailedElectionResult from './DetailedElectionResult';
import { getCountyElectionResults } from '@/api/counties';
import DetailedCountyChart from './DetailedCountyChart';
import { CountyResult, County } from '@/interfaces/county';
import CountyDemographicDetail from '../demographic/CountyDemographicDetail';

interface DetailedCountyProps {
	closeDialog: () => void;
	detailedCountyData: County;
}

const DetailedCounty = (props: DetailedCountyProps) => {
	const [results, setResults] = useState<CountyResult[]>([]);
	const [showDemographics, setShowDemographics] = useState(false);

	// Fetch election results for selected year
	const { data: resultsData, isPending: resultsPending } = getCountyElectionResults(
		props.detailedCountyData.name,
		props.detailedCountyData.fips,
	);

	// Update result when new data arrives
	useEffect(() => {
		if (!resultsPending && resultsData?.length) {
			setResults(resultsData);
		}
	}, [resultsData, resultsPending]);

	if (resultsPending && !results) return <div>Loading results...</div>;

	return (
		<div className="fixed inset-0 z-10 w-screen h-screen overflow-y-auto">
			<DialogBackdrop className="fixed inset-0 bg-black/40 backdrop-blur-sm transition-opacity" />
			<div className="flex min-h-full items-center justify-center p-4">
				<DialogPanel
					autoFocus
					className="w-full max-w-7xl h-full bg-white/90 rounded-none shadow-xl ring-1 ring-white/20 backdrop-blur-2xl overflow-y-auto p-6 flex flex-col"
				>
					
					{/* Header */}
					<h2 className="text-2xl font-bold text-purple-600 mb-6">
						{props.detailedCountyData.name} County Results
					</h2>

					{/* Horizontal scroll of election results */}
					<div className="flex space-x-6 overflow-x-auto pb-4">
						{results.map(result => (
							<DetailedElectionResult
								key={result.year + result.election}
								result={result}
							/>
						))}
					</div>

					{/* Margin trend chart */}
					<div className="mt-6 mb-8">
						<DetailedCountyChart results={results} />
					</div>

					{/* Toggle demographics */}
					<div className="mb-8">
						<button
							onClick={() => setShowDemographics(!showDemographics)}
							className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold shadow transition-colors
								${showDemographics ? 'bg-purple-600 text-white hover:bg-purple-700' : 'bg-gray-200 text-gray-800 hover:bg-gray-300'}`}
						>
							{showDemographics ? 'Hide Demographics' : 'Show Demographics'}
							<svg
								className={`w-4 h-4 transform transition-transform ${showDemographics ? 'rotate-90' : ''}`}
								fill="none"
								stroke="currentColor"
								strokeWidth={2}
								viewBox="0 0 24 24"
							>
								<path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
							</svg>
						</button>

						{showDemographics && (
							<div className="mt-6">
								<CountyDemographicDetail detailedCountyData={props.detailedCountyData} />
							</div>
						)}
					</div>

					{/* Close button */}
					<button
						type="button"
						className="rounded-lg bg-red-600 px-4 py-2 font-bold text-white shadow hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-400"
						onClick={props.closeDialog}
					>
						Close
					</button>
				</DialogPanel>
			</div>
		</div>
	);
};

export default memo(DetailedCounty);
