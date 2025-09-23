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
import { PopulationData } from "@/interfaces/population";

type PopulationCountyChartProps = {
  populationResults: PopulationData[];
};

const metrics = [
  "POPESTIMATE",
  "BIRTHS",
  "DEATHS",
  "INTERNATIONALMIG",
  "DOMESTICMIG",
  "NETMIG",
];

const colors: Record<string, string> = {
  POPESTIMATE: "#1f77b4",
  BIRTHS: "#2ca02c",
  DEATHS: "#d62728",
  INTERNATIONALMIG: "#9467bd",
  DOMESTICMIG: "#ff7f0e",
  NETMIG: "#17becf",
};

const PopulationCountyChart = (props: PopulationCountyChartProps) => {
    const [highlightMetric, setHighlightMetric] = useState<string | null>(null);
    const [hiddenMetrics, setHiddenMetrics] = useState<string[]>([]);

    // Transform populationResults into chart-ready data
    const chartData = useMemo(() => {
        if (!props.populationResults.length) return [];

        const years = Array.from(
        new Set(
            Object.keys(props.populationResults[0])
            .filter((key) => /\d{4}$/.test(key))
            .map((key) => key.slice(-4))
        )
        ).sort();

        return years.map((year) => {
        const row: Record<string, any> = { year };
        metrics.forEach((metric) => {
                const value =props.populationResults[0][`${metric}${year}` as keyof PopulationData];
                row[metric] = typeof value === "number" ? value : 0;
            });
            return row;
        });
    }, [props.populationResults]);

    // Sort metrics by total values across all years
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

    // Legend click toggles hidden state
    const handleLegendClick = (o: any) => {
        const { dataKey } = o;
        setHiddenMetrics((prev) =>
        prev.includes(dataKey) ? prev.filter((m) => m !== dataKey) : [...prev, dataKey]
        );
    };

    const toggleAllMetrics = () => {
        if (hiddenMetrics.length === 0) {
            // All visible → hide all
            setHiddenMetrics([...metrics]);
        } else {
            // Some hidden → show all
            setHiddenMetrics([]);
        }
    };

    const visibleMetrics = useMemo(
        () => metrics.filter((m) => !hiddenMetrics.includes(m)),
        [hiddenMetrics]
    );

    const yAxisDomain = useMemo(() => {
        if (!chartData.length || !visibleMetrics.length) return [0, 0];

        let min = Infinity;
        let max = -Infinity;

        chartData.forEach((row) => {
            visibleMetrics.forEach((metric) => {
                const value = row[metric] as number;
                if (value < min) min = value;
                if (value > max) max = value;
            });
        });

        return [Math.floor(min * 0.95), Math.ceil(max * 1.05)]; // Add some padding
    }, [chartData, visibleMetrics]);

    return (
        <div className="p-6 bg-white rounded-2xl shadow-lg border border-gray-200">
            <h2 className="text-2xl font-extrabold text-gray-800 tracking-tight mb-4">
                Population Trends
            </h2>

            <button
                onClick={toggleAllMetrics}
                className="ml-2 px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            >
                {hiddenMetrics.length === 0 ? "Deselect All" : "Select All"}
            </button>

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
                            stroke={colors[metric]}
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

export default PopulationCountyChart;
