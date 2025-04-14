import './App.css';
import { useState, useEffect } from 'react';
import incomeStatement from './assets/company.json';

function RowVal({item}: {item: number | null}){
    return  item ? item/1000 : " - "
}

function Model_Output_Page({setPageIndex}){
    return(
        <div>
        <div>
            <table>
                <label>Predicted Cash Flow</label>
                <tr>
                    <th scope="col"></th>
                </tr>
                <tr>
                    <th scope="row">Net Income/Loss</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Total Depreciation And Amoritization - Cash Flow</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Other Non-Cash Items</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Total Non-Cash Items</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Change In Accounts Recievable</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Change In Inventories</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Change In Accounts Payable</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Change In Assets/Liabilities</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Total Change In Assets/Liabilities</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Cash Flow From Operating Activites</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Change In Property. Play, And Equipment</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Change In Intangible Assets</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Acquisitions/Divestiures</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Change In Short-term Investments</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Change In Long-term Investments</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Change In Investments - Total</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Investing Activities - Other</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Cash Flow From Investing Activities</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Long-Term Debt</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Current Debt</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Debt Issuance/Retirement Net - Total</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Common Equity Issued/Repurchased</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Total Equity Issued/Repurchased</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Total Common And Preferred Stock Dividends Paid</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Financial Activities - Other</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Cash Flow From Financial Activities</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Net Cash Flow</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Stock-Based Compensation</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <th scope="row">Common Stock Dividend Paid</th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            </table>
        </div>
        </div>
    )

}

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
        setPageIndex(2);
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

function User_Model_Input_Page({setPageIndex}){
    const data = incomeStatement
    
    //Income statement
    const years = data.income_statement.map(item => item.YearAndQuarter)
    const costOfGoodsSold = data.income_statement.map(item => item.cogs)
    const grossProfit = data.income_statement.map(item => item.gross_profit)
    const netIncome = data.income_statement.map(item => item.net_income)

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
        setPageIndex(3);
        //alert(inputs);
    }
    
    return(
        <div>
        <h1>{data.ticker} Financal Data Selection</h1>
        <div id="table_div">
            <table>
                <label>Income Statement</label>
                <tr>
                    <th scope="col"></th>
                    {years.map((year) => (<th scope="col">{year}</th>))}
                </tr>
                <tr>
                    <th scope="row">Cost Of Goods Sold</th>

                    {costOfGoodsSold.map((cogs) => (
                        <td>$<RowVal item={cogs} /></td>
                        ))}
                </tr>
                <tr>
                    <th scope="row">Gross Profit</th>

                    {grossProfit.map((gp) => (
                        <td>$<RowVal item={gp} /></td>
                        ))}
                </tr>
                <tr>
                    <th scope="row">Net Income</th>

                    {netIncome.map((ni) => (
                        <td>$<RowVal item={ni} /></td>
                        ))}
                </tr>
            </table>
        </div>

        <br></br>
        <br></br>

        <div>
            <form onSubmit={handleSubmit}>
                <label>Select the Income Statement parameter(s) for model:<br></br>
                    <input type="checkbox" id="revenue" name="revenue" value="revenue" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="revenue">Revenue</label><br></br>
                    <input type="checkbox" id="costOfGoodsSold" name="costOfGoodsSold" value="costOfGoodsSold" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="costOfGoodsSold">Cost Of Goods Sold</label><br></br>
                    <input type="checkbox" id="grossProfit" name="grossProfit" value="grossProfit" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="grossProfit">Gross Profit</label><br></br>
                    <input type="checkbox" id="researchAndDevelopmentExpenses" name="researchAndDevelopmentExpenses" value="researchAndDevelopmentExpenses" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="researchAndDevelopmentExpenses">Research and Development Expenses</label><br></br>
                    <input type="checkbox" id="SG&A_Expenses" name="SG&A_Expenses" value="SG&A_Expenses" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="SG&A_Expenses">SG&A Expenses</label><br></br>
                    <input type="checkbox" id="otherOperatingIncomeOrExpenses" name="otherOperatingIncomeOrExpenses" value="otherOperatingIncomeOrExpenses" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="otherOperatingIncomeOrExpenses">Other Operating Income Or Expenses</label><br></br>
                    <input type="checkbox" id="operatingExpenses" name="operatingExpenses" value="operatingExpenses" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="operatingExpenses">Operating Expenses</label><br></br>
                    <input type="checkbox" id="operatingIncome" name="operatingIncome" value="operatingIncome" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="operatingIncome">Operating Income</label><br></br>
                    <input type="checkbox" id="totalNonOperatingIncomeOrExpenses" name="totalNonOperatingIncomeOrExpenses" value="totalNonOperatingIncomeOrExpenses" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalNonOperatingIncomeOrExpenses">Total Non-Operating Income/Expenses</label><br></br>
                    <input type="checkbox" id="preTaxIncome" name="preTaxIncome" value="preTaxIncome" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="preTaxIncome">Pre-Tax Income</label><br></br>
                    <input type="checkbox" id="incomeTaxes" name="incomeTaxes" value="incomeTaxes" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="incomeTaxes">Income Taxes</label><br></br>
                    <input type="checkbox" id="incomeAfterTaxes" name="incomeAfterTaxes" value="incomeAfterTaxes" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="incomeAfterTaxes">Income After Taxes</label><br></br>
                    <input type="checkbox" id="otherIncome" name="otherIncome" value="otherIncome" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="otherIncome">Other Income</label><br></br>
                    <input type="checkbox" id="incomeFromContinousOperations" name="incomeFromContinousOperations" value="incomeFromContinousOperations" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="incomeFromContinousOperations">Income From Continous Operations</label><br></br>
                    <input type="checkbox" id="incomeFromDiscontinuedOperations" name="incomeFromDiscontinuedOperations" value="incomeFromDiscontinuedOperations" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="incomeFromDiscontinuedOperations">Income From Discontinued Operations</label><br></br>
                    <input type="checkbox" id="netIncome" name="netIncome" value="netIncome" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netIncome">Net Income</label><br></br>
                    <input type="checkbox" id="EBITDA" name="EBITDA" value="EBITDA" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="EBITDA">EBITDA</label><br></br>
                    <input type="checkbox" id="EBIT" name="EBIT" value="EBIT" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="EBIT">EBIT</label><br></br>
                    <input type="checkbox" id="basicSharesOutstanding" name="basicSharesOutstanding" value="basicSharesOutstanding" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="basicSharesOutstanding">Basic Shares Outstanding</label><br></br>
                    <input type="checkbox" id="sharesOutstanding" name="sharesOutstanding" value="sharesOutstanding" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="sharesOutstanding">Shares Outstanding</label><br></br>
                    <input type="checkbox" id="basicEPS" name="basicEPS" value="basicEPS" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="basicEPS">Basic EPS</label><br></br>
                    <input type="checkbox" id="EPS_EarningsPerShare" name="EPS_EarningsPerShare" value="EPS_EarningsPerShare" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="EPS_EarningsPerShare">EPS - Earnings Per Share</label><br></br>
                   
                </label>

                <br></br>

                <label>Select the Balance Sheet parameter(s) for model:<br></br>
                    <input type="checkbox" id="cashOnHand" name="cashOnHand" value="cashOnHand" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="cashOnHand">Cash On Hand</label><br></br>
                    <input type="checkbox" id="recievables" name="recievables" value="recievables" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="recievables">Recievables</label><br></br>
                    <input type="checkbox" id="inventory" name="inventory" value="inventory" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="inventory">Inventory</label><br></br>
                    <input type="checkbox" id="prePaidExpenses" name="prePaidExpenses" value="prePaidExpenses" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="prePaidExpenses">Pre-Paid Expenses</label><br></br>
                    <input type="checkbox" id="otherCurrentAssets" name="otherCurrentAssets" value="otherCurrentAssets" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="otherCurrentAssets">Other Current Assets</label><br></br>
                    <input type="checkbox" id="totalCurrentAssets" name="totalCurrentAssets" value="totalCurrentAssets" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalCurrentAssets">Total Current Assets</label><br></br>
                    <input type="checkbox" id="propertyPlantAndEquipment" name="propertyPlantAndEquipment" value="propertyPlantAndEquipment" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="propertyPlantAndEquipment">Property, Plant, And Equipment</label><br></br>
                    <input type="checkbox" id="longTermInvestments" name="longTermInvestments" value="longTermInvestments" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="longTermInvestments">Long-Term Investments</label><br></br>
                    <input type="checkbox" id="goodwillAndIntangibleAssets" name="goodwillAndIntangibleAssets" value="goodwillAndIntangibleAssets" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="goodwillAndIntangibleAssets">Goodwill And Intangible Assets</label><br></br>
                    <input type="checkbox" id="otherLongTermInvestments" name="otherLongTermInvestments" value="otherLongTermInvestments" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="otherLongTermInvestments">Other Long-Term Investments</label><br></br>
                    <input type="checkbox" id="totalLongTermAssets" name="totalLongTermAssets" value="totalLongTermAssets" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalLongTermAssets">Total Long-Term Assets</label><br></br>
                    <input type="checkbox" id="totalAssets" name="totalAssets" value="totalAssets" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalAssets">Total Assets</label><br></br>
                    <input type="checkbox" id="totalCurrentLiabilities" name="totalCurrentLiabilities" value="totalCurrentLiabilities" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalCurrentLiabilities">Total Current Liabilities</label><br></br>
                    <input type="checkbox" id="longTermDebt" name="longTermDebt" value="longTermDebt" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="longTermDebt">Long-Term Debt</label><br></br>
                    <input type="checkbox" id="otherNonCurrentLiabilities" name="otherNonCurrentLiabilities" value="otherNonCurrentLiabilities" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="otherNonCurrentLiabilities">Other Non-Current Liabilities</label><br></br>
                    <input type="checkbox" id="totalLongTermLiabilities" name="totalLongTermLiabilities" value="totalLongTermLiabilities" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalLongTermLiabilities">Total Long-Term Liabilities</label><br></br>
                    <input type="checkbox" id="totalLiabilities" name="totalLiabilities" value="totalLiabilities" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalLiabilities">Total Liabilities</label><br></br>
                    <input type="checkbox" id="commonStockNet" name="commonStockNet" value="commonStockNet" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="commonStockNet">Common Stock Net</label><br></br>
                    <input type="checkbox" id="retainedEarnings" name="retainedEarnings" value="retainedEarnings" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="retainedEarnings">Retained Earnings (Accumulated Deficit)</label><br></br>
                    <input type="checkbox" id="comprehensiveIncome" name="comprehensiveIncome" value="comprehensiveIncome" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="comprehensiveIncome">Comprehensive Income</label><br></br>
                    <input type="checkbox" id="otherShareHoldersEquity" name="otherShareHoldersEquity" value="otherShareHoldersEquity" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="otherShareHoldersEquity">Other Share Holders Equity</label><br></br>
                    <input type="checkbox" id="shareHolderEquity" name="shareHolderEquity" value="shareHolderEquity" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="shareHolderEquity">Share Holder Equity</label><br></br>
                    <input type="checkbox" id="totalLiabilitiesAndShareHolderEquity" name="totalLiabilitiesAndShareHolderEquity" value="totalLiabilitiesAndShareHolderEquity" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalLiabilitiesAndShareHolderEquity">Total Liabilities And Share Holder Equity</label><br></br>
                </label>

                <br></br>

                <label>Select the Cash Flow parameter(s) for model:<br></br>
                    <input type="checkbox" id="netIncomeOrLoss" name="netIncomeOrLoss" value="netIncomeOrLoss" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netIncomeOrLoss">Net Income/Loss</label><br></br>
                    <input type="checkbox" id="totalDepreciationAndAmoritization" name="totalDepreciationAndAmoritization" value="totalDepreciationAndAmoritization" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalDepreciationAndAmoritization">Total Depreciation And Amoritization - Cash Flow</label><br></br>
                    <input type="checkbox" id="otherNonCashItems" name="otherNonCashItems" value="otherNonCashItems" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="otherNonCashItems">Other Non-Cash Items</label><br></br>
                    <input type="checkbox" id="totalNonCashItems" name="totalNonCashItems" value="totalNonCashItems" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalNonCashItems">Total Non-Cash Items</label><br></br>
                    <input type="checkbox" id="changeInAccountsRecievable" name="changeInAccountsRecievable" value="changeInAccountsRecievable" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="changeInAccountsRecievable">Change In Accounts Recievable</label><br></br>
                    <input type="checkbox" id="changeInInventories" name="changeInInventories" value="changeInInventories" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="changeInInventories">Change In Inventories</label><br></br>
                    <input type="checkbox" id="changeInAccountsPayable" name="changeInAccountsPayable" value="changeInAccountsPayable" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="changeInAccountsPayable">Change In Accounts Payable</label><br></br>
                    <input type="checkbox" id="changeInAssetsOrLiabilities" name="changeInAssetsOrLiabilities" value="changeInAssetsOrLiabilities" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="changeInAssetsOrLiabilities">Change In Assets/Liabilities</label><br></br>
                    <input type="checkbox" id="totalChangeInAssetsOrLiabilities" name="totalChangeInAssetsOrLiabilities" value="totalChangeInAssetsOrLiabilities" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalChangeInAssetsOrLiabilities">Total Change In Assets/Liabilities</label><br></br>
                    <input type="checkbox" id="cashFlowFromOperatingActivites" name="cashFlowFromOperatingActivites" value="cashFlowFromOperatingActivites" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="cashFlowFromOperatingActivites">Cash Flow From Operating Activites</label><br></br>
                    <input type="checkbox" id="netChangeInPropertyPlayAndEquipment" name="netChangeInPropertyPlayAndEquipment" value="netChangeInPropertyPlayAndEquipment" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netChangeInPropertyPlayAndEquipment">Net Change In Property. Play, And Equipment	</label><br></br>
                    <input type="checkbox" id="netChangeInIntangibleAssets" name="netChangeInIntangibleAssets" value="netChangeInIntangibleAssets" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netChangeInIntangibleAssets">Net Change In Intangible Assets</label><br></br>
                    <input type="checkbox" id="netAcquisitionsOrDivestiures	" name="netAcquisitionsOrDivestiures" value="netAcquisitionsOrDivestiures" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netAcquisitionsOrDivestiures">Net Acquisitions/Divestiures</label><br></br>
                    <input type="checkbox" id="netChangeInShortTermInvestments" name="netChangeInShortTermInvestments" value="netChangeInShortTermInvestments" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netChangeInShortTermInvestments">Net Change In Short-term Investments</label><br></br>
                    <input type="checkbox" id="netChangeInLongTermInvestments" name="netChangeInLongTermInvestments" value="netChangeInLongTermInvestments" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netChangeInLongTermInvestments">Net Change In Long-term Investments</label><br></br>
                    <input type="checkbox" id="netChangeInInvestmentsTotal" name="netChangeInInvestmentsTotal" value="netChangeInInvestmentsTotal" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netChangeInInvestmentsTotal">Net Change In Investments - Total</label><br></br>
                    <input type="checkbox" id="investingActivitiesOther" name="investingActivitiesOther" value="investingActivitiesOther" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="investingActivitiesOther">Investing Activities - Other</label><br></br>
                    <input type="checkbox" id="cashFlowFromInvestingActivities" name="cashFlowFromInvestingActivities" value="cashFlowFromInvestingActivities" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="cashFlowFromInvestingActivities">Cash Flow From Investing Activities</label><br></br>
                    <input type="checkbox" id="netLongTermDebt" name="netLongTermDebt" value="netLongTermDebt" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netLongTermDebt">Net Long-Term Debt</label><br></br>
                    <input type="checkbox" id="netCurrentDebt" name="netCurrentDebt" value="netCurrentDebt" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netCurrentDebt">Net Current Debt</label><br></br>
                    <input type="checkbox" id="debtIssuanceOrRetirementNetTotal" name="debtIssuanceOrRetirementNetTotal" value="debtIssuanceOrRetirementNetTotal" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="debtIssuanceOrRetirementNetTotal">Debt Issuance/Retirement Net - Total</label><br></br>
                    <input type="checkbox" id="netCommonEquityIssuedOrRepurchased" name="netCommonEquityIssuedOrRepurchased" value="netCommonEquityIssuedOrRepurchased" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netCommonEquityIssuedOrRepurchased">Net Common Equity Issued/Repurchased</label><br></br>
                    <input type="checkbox" id="netTotalEquityIssuedOrRepurchased" name="netTotalEquityIssuedOrRepurchased" value="netTotalEquityIssuedOrRepurchased" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netTotalEquityIssuedOrRepurchased">Net Total Equity Issued/Repurchased</label><br></br>
                    <input type="checkbox" id="totalCommonAndPreferredStockDividendsPaid" name="totalCommonAndPreferredStockDividendsPaid" value="totalCommonAndPreferredStockDividendsPaid" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="totalCommonAndPreferredStockDividendsPaid">Total Common And Preferred Stock Dividends Paid</label><br></br>
                    <input type="checkbox" id="financialActivitiesOther" name="financialActivitiesOther" value="financialActivitiesOther" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="financialActivitiesOther">Financial Activities - Other</label><br></br>
                    <input type="checkbox" id="cashFlowFromFinancialActivities" name="cashFlowFromFinancialActivities" value="cashFlowFromFinancialActivities" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="cashFlowFromFinancialActivities">Cash Flow From Financial Activities</label><br></br>
                    <input type="checkbox" id="netCashFlow" name="netCashFlow" value="netCashFlow" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="netCashFlow">Net Cash Flow</label><br></br>
                    <input type="checkbox" id="stockBasedCompensation" name="stockBasedCompensation" value="stockBasedCompensation" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="stockBasedCompensation">Stock-Based Compensation</label><br></br>
                    <input type="checkbox" id="commonStockDividendPaid" name="commonStockDividendPaid" value="commonStockDividendPaid" onChange={handleChange} defaultChecked={true}></input>
                    <label htmlFor="commonStockDividendPaid">Common Stock Dividend Paid</label><br></br>

                </label>

                <input type="submit" />
            </form>
        </div>
        </div>
    )
}

function App() {
    const [pageIndex, setPageIndex] = useState<number>(0);

    const Pages = Object.freeze({
        Start_Page: 0,
        Ticker_Enter_Page: 1,
        User_Select_Page: 2,
        Model_Output_Page: 3,
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
                        <h3>About</h3>
                        <p>
                            The PANAR Financial Model is a quantitative financial model that aims to aid financial analysts in valuing publicly traded companies. 
                        </p>
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
                        <Ticker_Enter_Page_Form setPageIndex={setPageIndex}/>
                    </div>
                </div>
            );
        case Pages.User_Select_Page:
            return(
                <div>
                    <div>
                        <User_Model_Input_Page setPageIndex={setPageIndex}/>
                    </div>
                </div>
            );
        case Pages.Model_Output_Page:
            return(
                <div>
                    <div>
                        <h1>Model Predictions</h1>
                        <Model_Output_Page setPageIndex={setPageIndex}/>
                    </div>
                </div>
            );
    }
}

export default App
