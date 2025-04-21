import './App.css'
import { useState, useEffect } from 'react';
import { 
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from "chart.js/auto";

ChartJS.register(CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend);
import {Line} from "react-chartjs-2";
import zoomPlugin from "chartjs-plugin-zoom";
import 'chartjs-adapter-date-fns';
ChartJS.register(zoomPlugin);


function Ticker_Enter_Page_Form({ setPageIndex, setDcfOutput, setTicker }) {
    const [inputs, setInputs] = useState({
        tick: "",
        model: "",
    });

    const handleChange = (event: any) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({ ...values, [name]: value }))
    }

    const handleSubmit = async (event: any) => {
        event.preventDefault();

        try {

            const response = await fetch('http://localhost:8000/initialize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(inputs),
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            console.log("Backend response:", data);

            setTicker(inputs.tick);
            setDcfOutput(data);
            // Navigate to the model output page
            setPageIndex(1);
        } catch (error) {
            console.error("Failed to submit ticker/model:", error);
            alert("Something went wrong sending your request.");
        }
    }

    return (
        <div style={{ scale: 3 }}>
            <form onSubmit={handleSubmit}>
                <label>Enter the company ticker:&nbsp;
                    <input
                        type="text"
                        name="tick"
                        value={inputs.tick || ""}
                        onChange={handleChange}
                        required
                    />
                </label>
                <br></br>
                <label>Select the model:<br></br>
                    <input type="radio" id="m1" name="model" value="Model 1" onChange={handleChange} required></input>
                    <label htmlFor="m1">Model 1</label><br></br>
                    <input type="radio" id="m2" name="model" value="Model 2" onChange={handleChange} required></input>
                    <label htmlFor="m2">Model 2</label><br></br>
                    <input type="radio" id="m3" name="model" value="Model 3" onChange={handleChange} required></input>
                    <label htmlFor="m3">Model 3</label>
                </label>
                <br></br>
                <input type="submit" />
            </form>
        </div>
    )
}
function FinancialStatementTable() {
    const [statementData, setStatementData] = useState<any[]>([]);

    useEffect(() => {
        fetch("http://localhost:8000/financial-statement")
            .then((res) => res.json())
            .then((data) => setStatementData(data))
            .catch((err) => console.error("Failed to load financial statement", err));
    }, []);

    if (statementData.length === 0) {
        return <p>Loading statement...</p>;
    }

    const metrics = [
        { key: "revenue", label: "Revenue" },
        { key: "cogs", label: "COGS" },
        { key: "gross_profit", label: "Gross Profit" },
        { key: "operating_expenses", label: "Operating Expenses" },
        { key: "net_income", label: "Net Income" },
    ];

    return (
        <div>
            <h2>Financial Statement</h2>
            <div id="table_div">
                <table border={1} cellPadding={8}>
                    <thead>
                        <tr>
                            <th>Metric</th>
                            {statementData.map((row, index) => (
                                <th key={index}>{row.YearAndQuarter}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {metrics.map((metric) => (
                            <tr key={metric.key}>
                                <td>{metric.label}</td>
                                {statementData.map((row, idx) => (
                                    <td key={idx}>
                                        {(row[metric.key] / 1e9).toFixed(2)}B
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

function FutureNetIncomeTable()
{
    const [fcfData, setfcfData] = useState<any[]>([]);

    useEffect(() => {
        fetch("http://localhost:8000/future-net-income")
            .then((res) => res.json())
            .then((data) => setfcfData(data))
            .catch((err) => console.error("Failed to load financial statement", err));
    }, []);

    if (fcfData.length === 0) {
        return <p>Loading future net income table...</p>;
    }
    
    return (
        <div>
            <h2>Future Net Income</h2>
            <div id="table_div">
                <table border={1} cellPadding={8}>
                    <thead>
                        <tr>
                            <th> </th>
                            { Object.keys(fcfData).map((key) => (
                                <th>{key}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td> </td>
                            { Object.keys(fcfData).map((key) => (
                                <td>{fcfData[key as keyof typeof fcfData]["0"]}</td>
                            ))}
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
}

function PriceChart(){
    const [priceChart, setPriceChart] = useState<any[]>([]);

    useEffect(() => {
        fetch("http://localhost:8000/price-chart")
            .then((res) => res.json())
            .then((data) => setPriceChart(data))
            .catch((err) => console.error("Failed to load price chart", err));
    }, []);

    if (priceChart.length === 0) {
        return <p>Loading Price Chart table...</p>;
    }

    const keys : string[] = Object.keys(priceChart["Close" as keyof typeof priceChart])

    return (
        <div>
            <h2>Price Chart</h2>
            <div>
                <Line
                    data={{
                        labels: keys.map((key) => key.substring(0, 10)),
                        datasets:[
                            {
                                label: "Price Chart",
                                data: keys.map((key) => priceChart["Close" as keyof typeof priceChart][key as keyof typeof priceChart])
                            },
                        ],
                    }} 
                />
            </div>
        </div>
    );

}

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

    const parsedData = current.dates.map((date: string, i: number) => ({
        date: new Date(date),
        value: current.values[i]
    })).filter((entry: any) => {
        const year = entry.date.getFullYear();
        return year >= startYear && year <= endYear;
    });

    const aggregatedData = aggregation === "annual"
        ? Object.values(parsedData.reduce((acc: any, entry: any) => {
            const year = entry.date.getFullYear();
            if (!acc[year]) acc[year] = { sum: 0, count: 0 };
            acc[year].sum += entry.value;
            acc[year].count++;
            return acc;
        }, {})).map((val: any, i: number, arr) => ({
            x: (1970 + i).toString(),
            y: val.sum / val.count
        }))
        : parsedData.map((entry: any) => ({
            x: entry.date.toISOString().split('T')[0],
            y: entry.value
        }));

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
                    labels: aggregatedData.map((d: any) => d.x),
                    datasets: [{
                        label: current.title,
                        data: aggregatedData.map((d: any) => d.y),
                        backgroundColor: chartType === "bar" ? "rgba(54, 162, 235, 0.6)" : "transparent",
                        borderColor: "rgba(75,192,192,1)",
                        fill: false
                    }]
                }}
                options={{
                    responsive: true,
                    plugins: {
                        tooltip: { mode: "index", intersect: false },
                        legend: { position: "top" },
                        zoom: {
                            zoom: {
                                wheel: { enabled: true },
                                pinch: { enabled: true },
                                mode: "x"
                            },
                            pan: {
                                enabled: true,
                                mode: "x"
                            }
                        }
                    },
                    scales: {
                        x: {
                            type: "time",
                            time: {
                                unit: aggregation === "monthly" ? "month" : "year"
                            },
                            ticks: {
                                autoSkip: true,
                                maxTicksLimit: 12
                            }
                        },
                        y: { beginAtZero: false }
                    }
                }}
                type={chartType}
            />
        </div>
    );
}

function App() {
    const [pageIndex, setPageIndex] = useState<number>(0);
    const [ticker, setTicker] = useState<string>("");
    const [dcfOutput, setDcfOutput] = useState<any>(null);
    const [selectedTable, setSelectedTable] = useState<"dcf" | "income" | "priceChart">("dcf");

    const Pages = Object.freeze({
        Ticker_Enter_Page: 0,
        Model_Output_Page: 1,
    });

    useEffect(() => {
        setPageIndex(JSON.parse(window.localStorage.getItem('pageIndex') || '{}'));
    }, []);

    useEffect(() => {
        window.localStorage.setItem('pageIndex', String(pageIndex));
    }, [pageIndex]);

    switch (pageIndex) {
        case Pages.Ticker_Enter_Page:
            return (
                <div>
                    <div>
                        <Ticker_Enter_Page_Form setPageIndex={setPageIndex} setDcfOutput={setDcfOutput} setTicker={setTicker} />
                    </div>
                </div>
            );
        case Pages.Model_Output_Page:
            return (
                <div style={{position: 'relative', top: '100px'}}>
                    <div className="header">
                        <h1> {ticker} </h1>

                        <div style={{ marginBottom: '1rem' }}>
                            <button onClick={() => setSelectedTable("income")}>Income Statement</button>
                            <button onClick={() => setSelectedTable("dcf")}>DCF Table</button>
                            <button onClick={() => setSelectedTable("priceChart")}>Price & Charts</button>
                        </div>

                        {selectedTable === "dcf" && dcfOutput ? (
                            <div>
                                <div style={{textAlign: 'center'}}>
                                    <h1> DCF Output </h1>
                                    {dcfOutput ? (
                                        <table>
                                            <thead>
                                                <tr><th>Metric</th><th>Value</th></tr>
                                            </thead>
                                            <tbody>
                                                {Object.entries(dcfOutput).map(([key, value]) => (
                                                    <tr key={key}>
                                                        <td>{key.replace(/_/g, ' ').toUpperCase()}</td>
                                                        <td>{typeof value === 'number' ? value.toFixed(2) : value}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    ) : (
                                        <p>No output available.</p>
                                    )}
                                </div>
                                <div>
                                    <FutureNetIncomeTable />
                                </div>
                            </div>
                        ) : selectedTable === "income" ? (
                            <div>
                                    <FinancialStatementTable />
                            </div>
                        ) : selectedTable === "priceChart" ? (
                            <div>
                                    <PriceChart />
                            </div>
                        ) : selectedTable === "bls" ? (
                            <div>
                                <BLSChart />
                            </div>
                        ) : (
                            <p>No data available</p>
                        )}
                    </div>
                </div>
            );
    }
}

export default App
