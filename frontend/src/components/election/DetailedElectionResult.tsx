'use client'

import { memo } from 'react'
import { CountyResult } from "@/interfaces/county"

interface DetailedElectionResultProps {
  result: CountyResult
}

const DetailedElectionResult = ({ result }: DetailedElectionResultProps) => {
  if (!result) return <div>No data available</div>

  const dVotes = parseInt(result.raw_votes_D, 10) || 0
  const rVotes = parseInt(result.raw_votes_R, 10) || 0
  const totalVotes = dVotes + rVotes

  let marginDisplay = ''
  let marginColor = ''
  let dPercent = 0
  let rPercent = 0

  if (totalVotes > 0) {
    dPercent = (dVotes / totalVotes) * 100
    rPercent = (rVotes / totalVotes) * 100
    const diff = Math.abs(dPercent - rPercent).toFixed(2)

    if (dPercent > rPercent) {
      marginDisplay = `D+${diff}`
      marginColor = 'text-blue-600'
    } else {
      marginDisplay = `R+${diff}`
      marginColor = 'text-red-600'
    }
  }

  return (
    <div className="w-64 flex-shrink-0 p-3 bg-white rounded-lg shadow">
      {/* Race title */}
      <p className="text-sm font-semibold text-gray-700 uppercase">
        {result.election} ({result.year})
      </p>

      {/* Democrat */}
      <div className="mt-1">
        <div className="text-blue-600 font-bold">{result.d_candidate}</div>
        <div className="text-gray-800 text-sm">{dVotes.toLocaleString()} votes</div>
      </div>

      {/* Republican */}
      <div className="mt-1">
        <div className="text-red-600 font-bold">{result.r_candidate}</div>
        <div className="text-gray-800 text-sm">{rVotes.toLocaleString()} votes</div>
      </div>

      {/* Margin */}
      {totalVotes > 0 && (
        <div className={`text-center font-bold mt-1 ${marginColor}`}>
          {marginDisplay}
        </div>
      )}

      {/* Progress bar */}
      {totalVotes > 0 && (
        <div className="w-full h-8 bg-gray-200 rounded overflow-hidden flex mt-2 shadow-inner text-white text-xs font-bold">
          <div
            className="bg-blue-500 flex items-center justify-center"
            style={{ width: `${dPercent}%` }}
          >
            {dPercent.toFixed(2)}%
          </div>
          <div
            className="bg-red-500 flex items-center justify-center"
            style={{ width: `${rPercent}%` }}
          >
            {rPercent.toFixed(2)}%
          </div>
        </div>
      )}
    </div>
  )
}

export default memo(DetailedElectionResult)
