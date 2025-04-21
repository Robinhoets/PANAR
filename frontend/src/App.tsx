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
                    <label htmlFor="m1">Linear Regression</label><br></br>
                    <input type="radio" id="m2" name="model" value="Model 2" onChange={handleChange} required></input>
                    <label htmlFor="m2">Gradient Boosting</label><br></br>
                    <input type="radio" id="m3" name="model" value="Model 3" onChange={handleChange} required></input>
                    <label htmlFor="m3">Neural Network</label>
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
    const [inputs, setInputs] = useState({
        fcfData: fcfData,
        model: "",
    });

    const handleChange = (event: any) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({ ...values, [name]: value }))
    }

    useEffect(() => {
        fetch("http://localhost:8000/future-net-income")
            .then((res) => res.json())
            .then((data) => setfcfData(data))
            .catch((err) => console.error("Failed to load financial statement", err));
    }, []);

    if (fcfData.length === 0) {
        return <p>Loading future net income table...</p>;
    }
    
    function handleEdit(event: any, index: number){
        const new_fcf_data = fcfData
        
        Object.keys(new_fcf_data).map((key, i) => {
            if(index == i){
                new_fcf_data[key as keyof typeof fcfData]["0"] = event.target.textContent
            } 
        });

        setfcfData(new_fcf_data)
        setInputs(values => ({ ...values, ["fcfData"]: fcfData }))

        Object.keys(fcfData).map((key, i) => {
            if(index == i){
                console.log(fcfData[key as keyof typeof fcfData]["0"])
            } 
        });
    }

    const handleSubmit = async (event: any) => {
        /*
        event.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/future-net-income', {
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
            
        } catch (error) {
            console.error("Failed to submit model\new data:", error);
            alert("Something went wrong sending your request.");
        }
        */
            
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
                            { Object.keys(fcfData).map((key, index) => (
                                <td contentEditable suppressContentEditableWarning={true} onInput={(e) => handleEdit(e, index)}>{fcfData[key as keyof typeof fcfData]["0"]}</td>
                            ))}
                        </tr>
                    </tbody>
                </table>
            </div>
            <div>
                <form onSubmit={handleSubmit}>
                    <label>Select the model:<br></br>
                        <input type="radio" id="m1" name="model" value="Model 1" onChange={handleChange} required></input>
                        <label htmlFor="m1">Linear Regression</label><br></br>
                        <input type="radio" id="m2" name="model" value="Model 2" onChange={handleChange} required></input>
                        <label htmlFor="m2">Gradient Boosting</label><br></br>
                        <input type="radio" id="m3" name="model" value="Model 3" onChange={handleChange} required></input>
                        <label htmlFor="m3">Neural Network</label>
                    </label>
                    <br></br>
                    <input type="submit" />
                </form>
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
                                label: "",
                                data: keys.map((key) => priceChart["Close" as keyof typeof priceChart][key as keyof typeof priceChart])
                            },
                        ],
                    }} 
                />
            </div>
        </div>
    );

}

function ModelInfo(){
    return(
        <div>
            <h1>About Models</h1>
            <div style={{textAlign: 'left'}}>
            <h2>Data Preparation</h2>
            <ul>
                <li>Numerical values include the five major income statement values. </li>
                <li>Categorical values are created with two algorithms: </li>
                    <ul style={{listStyleType: 'lower-alpha'}}>
                        <li> Quarterly data is processed with one-hot encoding, meaning every quarter is tracked as a binary value in four columns.</li>
                        <li> Year value and company ticker columns are processed with ordinal encoding, which essentially creates a dictionary mapping input values to integers. </li>
                    </ul>
            </ul>

            <h2>Model #1: Linear Regression </h2>
            <ul>
                <li>Very simple machine learning algorithm, creates relationships between linear values. </li>
                <li>
                    Has a tendency to be overly dependent on the trend of the first prediction quarter (negative yields negative downwards trend, while positive yields positive upwards trend). 
                </li>
            </ul>

            <h2>Model #2: Gradient Boosting </h2>
            <ul>
                <li>
                    Uses previous prediction’s gradient value in next prediction’s ‘tree’ structure to make decisions on important features of data. 
                </li>
                <li>
                    Tree’s prediction method is auto generated based on error minimization 
                </li>
                <li>
                    Tree has the objective of decreasing ‘squared error’ output of company net income with ‘root mean squared error’ (RSME) evaluation metric. 
                </li>
                <li>
                    Additional tree features include a maximum tree depth of 8 and a 1,000-step boosting round when training. 
                </li>
                    
            </ul>

            <h2>Model #3: Neural Network</h2>
            <ul>
                <li>
                    Uses three ‘Long Short-Term Memory’ layers (LSTM) to remember important values and features of input data, combined in a single dense output layer. Two of these ‘inner’ LSTM layers are hidden / black box operations.  
                </li>
                <li>
                    All LSTM layers use Rectified Linear Unit (RELU) activation functions to solve model issues of the ‘vanishing gradient’ problem, which has been relevant in attempts to improve model performance. 
                </li>
                <li>
                    ‘Adaptive Moment Estimator’ (ADAM) optimizer is used in the network along with the ‘mean squared error’ loss function. 
                </li>
                <li>
                    Requires 150 epochs (passes) of all data into the network to minimize loss.  
                </li>
                    
            </ul>
            </div>
        </div>
    )
}

function App() {
    const [pageIndex, setPageIndex] = useState<number>(0);
    const [ticker, setTicker] = useState<string>("");
    const [dcfOutput, setDcfOutput] = useState<any>(null);
    const [selectedTable, setSelectedTable] = useState<"dcf" | "income" | "priceChart" | "modelInfo">("dcf");

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
                            <button onClick={() => setSelectedTable("priceChart")}>Price & Charts</button>
                            <button onClick={() => setSelectedTable("income")}>Income Statement</button>
                            <button onClick={() => setSelectedTable("dcf")}>DCF Table</button>
                            <button onClick={() => setSelectedTable("modelInfo")}>Models Info</button>
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
                        ) : selectedTable === "modelInfo" ? (
                            <div>
                                    <ModelInfo />
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
