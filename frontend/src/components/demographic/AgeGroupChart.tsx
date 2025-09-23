import React, { useState, useMemo } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { AgeGroupData } from "@/interfaces/age";

interface AgeGroupsCountyChartProps {
  ageGroupData: AgeGroupData[];
}

const ageGroups = [
  "20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59", 
  "60-64","65-69","70-74","75-79","80-84","85+"
];

// Generate colors for age groups
const colors = ageGroups.reduce((acc, grp, idx) => {
  acc[grp] = `hsl(${(idx / ageGroups.length) * 360}, 70%, 50%)`;
  return acc;
}, {} as Record<string, string>);

const AgeGroupsCountyChart = ( props: AgeGroupsCountyChartProps ) => {
  const [highlightGroup, setHighlightGroup] = useState<string | null>(null);
  const [hiddenGroups, setHiddenGroups] = useState<string[]>([]);

    // Transform data for chart
    const chartData = useMemo(() => {
    return props.ageGroupData
        .sort((a, b) => a.YEAR - b.YEAR)
        .map((row) => ({
        year: row.YEAR,
        ...ageGroups.reduce((acc, grp) => {
            acc[grp] = row[grp as keyof AgeGroupData] as number;
            return acc;
        }, {} as Record<string, number>)
        }));
    }, [props.ageGroupData]);


  // Toggle individual age group lines
  const handleLegendClick = (o: any) => {
    const { dataKey } = o;
    setHiddenGroups((prev) =>
      prev.includes(dataKey)
        ? prev.filter((g) => g !== dataKey)
        : [...prev, dataKey]
    );
  };

  // Toggle all age groups
  const toggleAllGroups = () => {
    if (hiddenGroups.length === 0) {
      setHiddenGroups([...ageGroups]);
    } else {
      setHiddenGroups([]);
    }
  };

  // compute dynamic Y axis domain based only on visible groups (returns a typed tuple)
  const yAxisDomain = useMemo<[number, number]>(() => {
    if (!chartData || !chartData.length) return [0, 0];

    let min = Number.POSITIVE_INFINITY;
    let max = Number.NEGATIVE_INFINITY;

    for (const row of chartData) {
      for (const grp of ageGroups) {
        if (hiddenGroups.includes(grp)) continue; // ignore hidden groups
        const raw = row[grp as keyof typeof row];
        const v = typeof raw === "number" ? raw : Number(raw);
        if (!Number.isFinite(v)) continue;            // skip NaN/undefined
        if (v < 0) continue;                          // skip placeholders like -1 (adjust if needed)
        if (v < min) min = v;
        if (v > max) max = v;
      }
    }

    if (min === Number.POSITIVE_INFINITY || max === Number.NEGATIVE_INFINITY) {
      // no valid data (all hidden or placeholders) — fallback
      return [0, 0];
    }

    // padding and safe fallback to ensure non-zero range
    const paddedMin = Math.max(0, Math.floor(min * 0.95));
    const paddedMax = Math.ceil(max * 1.05);
    if (paddedMin >= paddedMax) {
      return [Math.max(0, paddedMin - 1), paddedMax + 1];
    }
    return [paddedMin, paddedMax];
  }, [chartData, hiddenGroups]);

  return (
    <div className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-extrabold text-gray-800 tracking-tight">
          Age Group Population Trends
        </h2>

        <button
          onClick={toggleAllGroups}
          className="ml-2 px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
        >
          {hiddenGroups.length === 0 ? "Deselect All" : "Select All"}
        </button>
      </div>

      <ResponsiveContainer width="100%" height={420}>
        <LineChart data={chartData}>
          <XAxis dataKey="year" />
          <YAxis type="number" domain={yAxisDomain} allowDataOverflow/>
          <Tooltip
            formatter={(value, name) =>
              hiddenGroups.includes(name as string) ? null : [value, name]
            }
            labelClassName="text-lg font-bold text-gray-800"
          />

          <Legend
            verticalAlign="top"
            height={60}
            onClick={handleLegendClick}
            onMouseEnter={(o: any) => setHighlightGroup(o.dataKey)}
            onMouseLeave={() => setHighlightGroup(null)}
            formatter={(value: string) => {
              const isHidden = hiddenGroups.includes(value);
              return (
                <span
                  style={{
                    color: isHidden ? "#9ca3af" : colors[value],
                    fontWeight: isHidden ? "normal" : "bold",
                    cursor: "pointer",
                  }}
                >
                  {value}
                </span>
              );
            }}
          />

          {ageGroups.map((grp) => (
            <Line
              key={grp}
              type="monotone"
              dataKey={grp}
              stroke={colors[grp]}
              strokeWidth={highlightGroup === grp || highlightGroup === null ? 3 : 1.5}
              dot={false}
              opacity={
                hiddenGroups.includes(grp)
                  ? 0
                  : highlightGroup && highlightGroup !== grp
                  ? 0.3
                  : 1
              }
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AgeGroupsCountyChart;
