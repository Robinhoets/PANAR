import './App.css'
import { useState, useEffect } from 'react';

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

            const response = await fetch('http://localhost:8000/test', {
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

    return (
        <div>
            <h2>Financial Statement</h2>
            <table border={1} cellPadding={8}>
                <thead>
                    <tr>
                        <th>Year/Quarter</th>
                        <th>Revenue</th>
                        <th>COGS</th>
                        <th>Gross Profit</th>
                        <th>Operating Expenses</th>
                        <th>Net Income</th>
                    </tr>
                </thead>
                <tbody>
                    {statementData.map((row, index) => (
                        <tr key={index}>
                            <td>{row.YearAndQuarter}</td>
                            <td>{(row.revenue / 1e9).toFixed(2)}B</td>
                            <td>{(row.cogs / 1e9).toFixed(2)}B</td>
                            <td>{(row.gross_profit / 1e9).toFixed(2)}B</td>
                            <td>{(row.operating_expenses / 1e9).toFixed(2)}B</td>
                            <td>{(row.net_income / 1e9).toFixed(2)}B</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

function App() {
    const [pageIndex, setPageIndex] = useState<number>(0);
    const [ticker, setTicker] = useState<string>("");
    const [dcfOutput, setDcfOutput] = useState<any>(null);
    const [selectedTable, setSelectedTable] = useState<"dcf" | "income">("dcf");

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
                <div>
                    <div className="header">
                        <h1> T </h1>
                        <h1> {ticker} </h1>

                        <div style={{ marginBottom: '1rem' }}>
                            <button onClick={() => setSelectedTable("income")}>Income Statement</button>
                            <button onClick={() => setSelectedTable("dcf")}>DCF Table</button>
                        </div>

                        {selectedTable === "dcf" && dcfOutput ? (
                            <div>
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
                        ) : selectedTable === "income" ? (
                            <div>
                                    <FinancialStatementTable />
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
