import './App.css'
import { useState, useEffect } from 'react';

function Ticker_Enter_Page_Form({setPageIndex}) {
    const [inputs, setInputs] = useState({
        ticker : "",
        model : "",
    });
  
    const handleChange = (event : any) => {
      const name = event.target.name;
      const value = event.target.value;
      setInputs(values => ({...values, [name]: value}))
    }
  
    const handleSubmit = (event : any) => {
        event.preventDefault();

        try {
            const response = await fetch('http://localhost:8000/app/test', {
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

            // Navigate to the model output page
            setPageIndex(1);
        } catch (error) {
            console.error("Failed to submit ticker/model:", error);
            alert("Something went wrong sending your request.");
        }
    }
  
    return (
    <div style={{scale: 3}}>
        <form onSubmit={handleSubmit}>
            <label>Enter the company ticker:&nbsp;
            <input 
            type="text" 
            name="ticker" 
            value={inputs.ticker || ""} 
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

function App() {
    const [pageIndex, setPageIndex] = useState<number>(0);

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

    switch(pageIndex){
        case Pages.Ticker_Enter_Page:
            return(
                <div>
                    <div>
                        <Ticker_Enter_Page_Form setPageIndex={setPageIndex}/>
                    </div>
                </div>
            );
        case Pages.Model_Output_Page:
            return(
                <div>
                    <div className="header">
                        <h1>DCF Output</h1>
                        <h3>About</h3>
                        <p>
                            dcf output goes here
                        </p>
                    </div>
                </div>
            );
    }
}

export default App
