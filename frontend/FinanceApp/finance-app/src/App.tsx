import './App.css'
import { useState, useEffect } from 'react';

function Ticker_Enter_Page_Form() {
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
      //alert(inputs);
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
        Start_Page: 0,
        Ticker_Enter_Page: 1,
        User_Select_Page: 2,
    });

    useEffect(() => {
        setPageIndex(JSON.parse(window.localStorage.getItem('pageIndex') || '{}'));
      }, []);
    
    useEffect(() => {
    window.localStorage.setItem('pageIndex', String(pageIndex));
    }, [pageIndex]);

    switch(pageIndex){
        case Pages.Start_Page:
            return(
                <div>
                    <div className="header">
                        <h1>PANAR Financial Modeling App</h1>
                    </div>
                    <button 
                    className="startBtn"
                    onClick={() => setPageIndex(Pages.Ticker_Enter_Page)}
                    >
                        Start
                    </button>
                </div>
            );
        case Pages.Ticker_Enter_Page:
            return(
                <div>
                    <div>
                        <Ticker_Enter_Page_Form />
                    </div>
                </div>
            );
    }
}

export default App
