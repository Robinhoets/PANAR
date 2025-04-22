import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";

function BLSChart() {
    const [blsData, setBlsData] = useState<any>({});
    const [selectedSeries, setSelectedSeries] = useState<string>("LNS14000000");
    const [startYear, setStartYear] = useState<number>(1970);
    const [endYear, setEndYear] = useState<number>(2023);
    const [chartType, setChartType] = useState<"line" | "bar">("line");
    const [aggregation, setAggregation] = useState<"monthly" | "annual">("monthly");

    useEffect(() => {
        fetch("http://localhost:8000/bls-data")
            .then(res => res.json())
            .then(data => setBlsData(data))
            .catch(err => console.error("Failed to load BLS data", err));
    }, []);

    if (Object.keys(blsData).length === 0) {
        return <p>Loading BLS data...</p>;
    }

    const current = blsData[selectedSeries];
    if (!current) return <p>No data found for this series.</p>;

    // Parse and filter by year
    const parsedData = current.dates.map((date: string, i: number) => ({
        date: new Date(date),
        value: current.values[i]
    })).filter((entry: any) => {
        const year = entry.date.getFullYear();
        return year >= startYear && year <= endYear;
    });

    // Group and average by year if aggregation is annual
    let chartData: { x: string, y: number }[] = [];

    if (aggregation === "annual") {
        const grouped: Record<number, { sum: number, count: number }> = {};

        parsedData.forEach(({ date, value }: any) => {
            const year = date.getFullYear();
            if (!grouped[year]) grouped[year] = { sum: 0, count: 0 };
            grouped[year].sum += value;
            grouped[year].count += 1;
        });

        chartData = Object.entries(grouped)
            .map(([year, { sum, count }]) => ({
                x: year,
                y: sum / count
            }))
            .sort((a, b) => parseInt(a.x) - parseInt(b.x));  // Ensure chronological order
    } else {
        chartData = parsedData.map(({ date, value }) => ({
            x: date.toISOString().split('T')[0],
            y: value
        }));
    }

    return (
        <div>
            <h2>BLS Chart</h2>
            <div style={{ marginBottom: "1rem" }}>
                <label>Select Series: &nbsp;
                    <select value={selectedSeries} onChange={e => setSelectedSeries(e.target.value)}>
                        {Object.keys(blsData).map((seriesId) => (
                            <option key={seriesId} value={seriesId}>
                                {seriesId} - {blsData[seriesId].title}
                            </option>
                        ))}
                    </select>
                </label>
            </div>

            <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem", flexWrap: "wrap" }}>
                <div>
                    <label>Start Year: &nbsp;
                        <input
                            type="number"
                            value={startYear}
                            min="1970"
                            max="2023"
                            onChange={e => setStartYear(parseInt(e.target.value))}
                        />
                    </label>
                </div>
                <div>
                    <label>End Year: &nbsp;
                        <input
                            type="number"
                            value={endYear}
                            min="1970"
                            max="2023"
                            onChange={e => setEndYear(parseInt(e.target.value))}
                        />
                    </label>
                </div>
                <div>
                    <label>Chart Type: &nbsp;
                        <select value={chartType} onChange={e => setChartType(e.target.value as "line" | "bar")}>
                            <option value="line">Line</option>
                            <option value="bar">Bar</option>
                        </select>
                    </label>
                </div>
                <div>
                    <label>Aggregation: &nbsp;
                        <select value={aggregation} onChange={e => setAggregation(e.target.value as "monthly" | "annual")}>
                            <option value="monthly">Monthly</option>
                            <option value="annual">Annual Avg</option>
                        </select>
                    </label>
                </div>
            </div>

            <Line
                data={{
                    labels: chartData.map((d) => d.x),
                    datasets: [{
                        label: current.title,
                        data: chartData.map((d) => d.y),
                        fill: false,
                        tension: 0.2
                    }]
                }}
                options={{
                    responsive: true,
                    plugins: {
                        tooltip: { mode: "index", intersect: false },
                        legend: { position: "top" }
                    },
                    scales: {
                        x: {
                            type: aggregation === "annual" ? "category" : "time",
                            time: {
                                unit: aggregation === "annual" ? undefined : "month"
                            },
                            ticks: { autoSkip: true, maxTicksLimit: 12 }
                        },
                        y: { beginAtZero: false }
                    }
                }}
            />
        </div>
    );
}

export default BLSChart;
