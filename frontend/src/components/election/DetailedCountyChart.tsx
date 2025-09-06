'use client'

import { memo } from 'react'
import {
	CartesianGrid,
	LineChart,
	Line,
	Tooltip,
	ResponsiveContainer,
	ReferenceLine,
	XAxis,
	YAxis,
} from 'recharts'

import { CountyResult } from '@/api/electionResults'

const RACE_TYPES = ['President', 'Senate', 'Governor']

interface DetailedCountyChartProps {
  results: CountyResult[]
}

interface ChartDataPoint {
  year: string
  margin: number
}

const DetailedCountyChart = ({ results }: DetailedCountyChartProps) => {
	
	const raceData: Record<string, ChartDataPoint[]> = {}

	// Prepare data for each race
	RACE_TYPES.forEach(race => {
		raceData[race] = results
			.filter(r =>r.election.toLowerCase() === race.toLowerCase())
			.map(r => {
				const dVotes = parseInt(r.raw_votes_D) || 0
				const rVotes = parseInt(r.raw_votes_R) || 0
				const totalVotes = dVotes + rVotes
				const margin = totalVotes > 0 ? ((dVotes - rVotes) / totalVotes) * 100 : 0
				return { year: r.year, margin: parseFloat(margin.toFixed(2)) }
			})
	})

	// Custom dot to color each point based on margin
	const renderDot = (props: any) => {
		const { cx, cy, payload, index } = props
		const color = payload.margin >= 0 ? '#1f77b4' : '#d62728'
		return <circle key={`${payload.year}-${index}`} cx={cx} cy={cy} r={4} fill={color} stroke={color} />
	}

	// Custom tooltip formatter with D+/R+ label and color
	const tooltipFormatter = (value: number) => {
		const isDem = value >= 0
		const color = isDem ? '#1f77b4' : '#d62728'
		const label = isDem ? `D+${value.toFixed(2)}%` : `R+${Math.abs(value).toFixed(2)}%`
		return <span style={{ color, fontWeight: 'bold' }}>{label}</span>
	}

	return (
		<div className="flex gap-6 mt-4 w-full">
			{RACE_TYPES.map(race => {
				const data = raceData[race]
				if (!data.length) return null
				return (
					<div
						key={race}
						className="flex-1 h-80 bg-white rounded-lg shadow p-3 flex flex-col"
					>
						<h3 className="text-center font-semibold text-gray-700 uppercase mb-2">{race}</h3>
						<div className="flex-1">
							<ResponsiveContainer width="100%" height="100%">
								<LineChart
									data={data}
									margin={{ top: 5, right: 20, left: 0, bottom: 20 }}
								>
									<CartesianGrid strokeDasharray="3 3" />
									<XAxis dataKey="year" />
									<YAxis
										domain={(domain: [number, number]) => {
											const [dataMin, dataMax] = domain
											const absMax = Math.max(Math.abs(dataMin), Math.abs(dataMax))
											const rounded = Math.ceil(absMax)
											return [-rounded, rounded]
										}}
										tickFormatter={(val: number) => val.toFixed(0)}
									/>
									<ReferenceLine y={0} stroke="#000" strokeWidth={1.5} />
									<Tooltip
										formatter={tooltipFormatter}
										labelStyle={{ color: '#000', fontWeight: 'bold' }}
									/>
									<Line
										type="monotone"
										dataKey="margin"
										stroke="#999"
										strokeWidth={2}
										dot={renderDot}
										isAnimationActive={false}
									/>
								</LineChart>
							</ResponsiveContainer>
						</div>
					</div>
				)
			})}
		</div>
	)
}

export default memo(DetailedCountyChart)
