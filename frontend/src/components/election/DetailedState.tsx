'use client'

import { memo } from 'react'
import { getStateElectionResults } from '@/api/states'
import { StateResult } from '@/interfaces/state'

interface DetailedStateProps {
  stateName: string
}

const DetailedState = ({ stateName }: DetailedStateProps) => {
  const { data: results, isPending } = getStateElectionResults(stateName)

  if (isPending) return (
    <div className="absolute top-0 right-0 w-96 p-4 bg-white rounded-lg shadow-lg">
      Loading state results...
    </div>
  )

  if (!results?.length) return (
    <div className="absolute top-0 right-0 w-96 p-4 bg-white rounded-lg shadow-lg">
      No results available for {stateName}
    </div>
  )

  return (
    <div className="absolute top-0 right-0 w-96 max-h-[70vh] p-4 bg-white rounded-lg shadow-lg overflow-y-auto mb-12">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
        {stateName} Results
        </h2>

        {results.map((res: StateResult, idx: number) => {
            const dVotes = parseInt(res.raw_votes_D, 10) || 0
            const rVotes = parseInt(res.raw_votes_R, 10) || 0
            const totalVotes = dVotes + rVotes

            let marginDisplay = ''
            let marginColor = ''
            if (totalVotes > 0) {
            const dPct = (dVotes / totalVotes) * 100
            const rPct = (rVotes / totalVotes) * 100
            const diff = Math.abs(dPct - rPct).toFixed(2)

            if (dPct > rPct) {
                marginDisplay = `D+${diff}`
                marginColor = 'text-blue-600'
            } else {
                marginDisplay = `R+${diff}`
                marginColor = 'text-red-600'
            }
        }

        return (
          <div key={idx} className="mb-4 p-3 rounded-lg bg-gray-50 shadow-sm">
            <p className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-1">
              {res.election} ({res.year})
            </p>
            <div className="flex justify-between">
                <div className="mb-2">
                    <div className="text-blue-600 font-bold truncate" title={res.d_candidate}>
                        {res.d_candidate}
                    </div>
                    <div className="text-blue-500 text-sm">
                        Votes: {dVotes.toLocaleString()}
                    </div>
                </div>
                <div className="mb-2">
                    <div className="text-red-600 font-bold truncate" title={res.r_candidate}>
                        {res.r_candidate}
                    </div>
                    <div className="text-red-500 text-sm">
                        Votes: {rVotes.toLocaleString()}
                    </div>
                </div>
            </div>
            <div className={`text-center font-bold ${marginColor} mt-1`}>
              Margin: {marginDisplay}
            </div>
            {totalVotes > 0 && (
              <div className="w-full h-4 bg-gray-200 rounded overflow-hidden flex mt-1 shadow-inner">
                <div
                  className="bg-blue-500 h-full"
                  style={{ width: `${(dVotes / totalVotes) * 100}%` }}
                />
                <div
                  className="bg-red-500 h-full"
                  style={{ width: `${(rVotes / totalVotes) * 100}%` }}
                />
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

export default memo(DetailedState)
