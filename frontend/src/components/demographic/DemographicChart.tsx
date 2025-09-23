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
import { DemographicData } from "@/interfaces/demographic";

interface DemographicCountyChartProps {
  demographicResults: DemographicData[];
}

const metrics = [
  "TOT_POP",
  "TOT_MALE",
  "TOT_FEMALE",
  "WHITE_MALE",
  "WHITE_FEMALE",
  "BLACK_MALE",
  "BLACK_FEMALE",
  "ASIAN_MALE",
  "ASIAN_FEMALE",
  "HISPANIC_MALE",
  "HISPANIC_FEMALE",
];

const colors: Record<string, string> = {
  TOT_POP: "#2563eb", // blue
  TOT_MALE: "#16a34a", // green
  TOT_FEMALE: "#dc2626", // red
  WHITE_MALE: "#9333ea", // purple
  WHITE_FEMALE: "#a855f7",
  BLACK_MALE: "#f97316", // orange
  BLACK_FEMALE: "#fb923c",
  ASIAN_MALE: "#0ea5e9", // cyan
  ASIAN_FEMALE: "#06b6d4",
  HISPANIC_MALE: "#eab308", // yellow
  HISPANIC_FEMALE: "#facc15",
};

const DemographicCountyChart = ( props: DemographicCountyChartProps ) => {
    const [highlightMetric, setHighlightMetric] = useState<string | null>(null);
    const [selectedGroup, setSelectedGroup] = useState<string>("aggregate");
    const [hiddenMetrics, setHiddenMetrics] = useState<string[]>([]);


    // Unique age groups
    const allAgeGroups = useMemo(() => {
        const set = new Set<string>();
        props.demographicResults.forEach((r) => set.add(r.AGEGRP));
        return Array.from(set).sort();
    }, [props.demographicResults]);

    // Prepare chart data
    const chartData = useMemo(() => {
        if (!props.demographicResults.length) return [];

        const grouped: Record<number, any> = {};

        props.demographicResults
        .filter((r) =>
            selectedGroup === "aggregate" ? true : r.AGEGRP === selectedGroup
        )
        .forEach((row) => {
            const year = row.YEAR;
            if (!grouped[year]) {
            grouped[year] = { year, ...Object.fromEntries(metrics.map((m) => [m, 0])) };
            }
            metrics.forEach((metric) => {
            grouped[year][metric] += row[metric as keyof DemographicData] as number;
            });
        });

        return Object.values(grouped).sort((a, b) => a.year - b.year);
    }, [props.demographicResults, selectedGroup]);

    // Legend click toggles hidden state
    const handleLegendClick = (o: any) => {
        const { dataKey } = o;
        setHiddenMetrics((prev) =>
        prev.includes(dataKey)
            ? prev.filter((m) => m !== dataKey)
            : [...prev, dataKey]
        );
    };

    // Compute total values for sorting legend
    const metricTotals = useMemo(() => {
        const totals: Record<string, number> = {};
        metrics.forEach((metric) => {
            totals[metric] = chartData.reduce(
                (sum, row) => sum + (row[metric] as number),
                0
            );
        });
        return metrics.sort((a, b) => totals[b] - totals[a]);
    }, [chartData]);

    const toggleAllMetrics = () => {
        if (hiddenMetrics.length === 0) {
            // All visible → hide all
            setHiddenMetrics([...metrics]);
        } else {
            // Some hidden → show all
            setHiddenMetrics([]);
        }
    };

    // Dynamic Y-axis domain based on visible metrics
    const yAxisDomain = useMemo<[number, number]>(() => {
        if (!chartData || !chartData.length) return [0, 0];

        let min = Number.POSITIVE_INFINITY;
        let max = Number.NEGATIVE_INFINITY;

        for (const row of chartData) {
            for (const metric of metrics) {
                if (hiddenMetrics.includes(metric)) continue;
                const raw = row[metric];
                const v = typeof raw === "number" ? raw : Number(raw);
                if (!Number.isFinite(v)) continue;
                if (v < 0) continue; // skip placeholders
                if (v < min) min = v;
                if (v > max) max = v;
            }
        }

        if (min === Number.POSITIVE_INFINITY || max === Number.NEGATIVE_INFINITY) {
            return [0, 0]; // fallback if everything hidden
        }

        const paddedMin = Math.max(0, Math.floor(min * 0.95));
        const paddedMax = Math.ceil(max * 1.05);
        if (paddedMin >= paddedMax) {
            return [Math.max(0, paddedMin - 1), paddedMax + 1];
        }
        return [paddedMin, paddedMax];
    }, [chartData, hiddenMetrics]);


    return (
        <div className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-extrabold text-gray-800 tracking-tight">
                    Demographic Trends —{" "}
                    <span className="text-gray-800">
                        {selectedGroup === "aggregate" ? "Aggregate" : "Age Group: " + selectedGroup}
                    </span>
                </h2>

                {/* Group selector */}
                <div>
                    <label className="mr-3 font-semibold text-gray-700">Select Group:</label>
                    <select
                        value={selectedGroup}
                        onChange={(e) => setSelectedGroup(e.target.value)}
                        className="border rounded-lg px-3 py-2 shadow-sm focus:ring-2 focus:ring-blue-500 text-gray-800 font-medium"
                    >
                        <option value="aggregate">Aggregate (All Age Groups)</option>
                        {allAgeGroups.map((grp) => (
                            <option key={grp} value={grp}>
                                Age Group: {grp}
                            </option>
                        ))}
                    </select>
                </div>

                <button
                        onClick={toggleAllMetrics}
                        className="ml-2 px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
                    >
                        {hiddenMetrics.length === 0 ? "Deselect All" : "Select All"}
                </button>
            </div>

            <ResponsiveContainer width="100%" height={420}>
                <LineChart data={chartData}>
                    <XAxis dataKey="year" />
                    <YAxis type="number" domain={yAxisDomain} allowDataOverflow/>
                    <Tooltip
                        formatter={(value, name) =>
                            hiddenMetrics.includes(name as string) ? null : [value, name]
                        }
                        labelClassName="text-lg font-bold text-gray-800"
                    />

                    <Legend
                        verticalAlign="top"
                        height={60}
                        onClick={handleLegendClick}
                        onMouseEnter={(o: any) => setHighlightMetric(o.dataKey)}
                        onMouseLeave={() => setHighlightMetric(null)}
                        formatter={(value: string) => {
                            const isHidden = hiddenMetrics.includes(value);
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

                    {metricTotals.map((metric) => (
                        <Line
                        key={metric}
                        type="monotone"
                        dataKey={metric}
                        stroke={colors[metric] || "#000"}
                        strokeWidth={highlightMetric === metric || highlightMetric === null ? 3 : 1.5}
                        dot={false}
                        opacity={
                            hiddenMetrics.includes(metric)
                            ? 0
                            : highlightMetric && highlightMetric !== metric
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

export default DemographicCountyChart;
