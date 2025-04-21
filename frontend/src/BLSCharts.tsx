import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";

function BLSChart() {
    const [charts, setCharts] = useState<any[]>([]);
    const [selectedChartIndex, setSelectedChartIndex] = useState<number | null>(null);

    useEffect(() => {
        fetch("http://localhost:8000/bls-data")
            .then((res) => res.json())
            .then((data) => setCharts(data))
            .catch((err) => console.error("Failed to load BLS data", err));
    }, []);

    if (charts.length === 0) return <p>Loading BLS data...</p>;

    const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedChartIndex(Number(event.target.value));
    };

    return (
        <div>
            <h2>BLS Charts</h2>
            <select onChange={handleChange} style={{ fontSize: "1rem", padding: "0.5rem", marginBottom: "1rem" }}>
                <option value="">-- Select a data series --</option>
                {charts.map((chart, index) => (
                    <option key={index} value={index}>
                        {chart.title}
                    </option>
                ))}
            </select>

            {selectedChartIndex !== null && charts[selectedChartIndex] && (
                <div>
                    <h3>{charts[selectedChartIndex].title}</h3>
                    <Line
                        data={{
                            labels: charts[selectedChartIndex].dates,
                            datasets: [
                                {
                                    label: charts[selectedChartIndex].title,
                                    data: charts[selectedChartIndex].values,
                                    fill: false,
                                },
                            ],
                        }}
                    />
                </div>
            )}
        </div>
    );
}

export default BLSChart;
