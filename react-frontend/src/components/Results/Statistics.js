import React, { useEffect, useState } from "react";
import {Container} from "react-bootstrap";
import axios from "axios";
import "./Results.css"

function Statistics() {
  
  const [stock, setStock] = useState([]);

  const requestBody = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json'},
    name: 'AAPL'
  }

  useEffect(() => {
    axios.post('/api/result/stats', requestBody)
      .then(res => {
        const response = JSON.parse(JSON.stringify(res.data));
        setStock({
          companyName: response['longName'],
          logo: response['logo_url'],
          symbol: response['symbol'],
          openPrice: '$' +response['open'],
          dayHigh: '$' + response['dayHigh'],
          dayLow: '$' + response['dayLow'],
          fiftyTwoWeekHigh: '$' + response['fiftyTwoWeekHigh'],
          fiftyTwoWeekLow: '$' + response['fiftyTwoWeekLow'],
          volume: response['volume'],
          avgVolume: response['averageVolume'],
          marketCap: '$' + getNumberUnit(response['marketCap']),
          pegRatio: (response['pegRatio']).toFixed(2),
          divYield: (response['dividendYield'] * 100).toFixed(2)
        });

        console.log(response);
      });
      
      
  }, []);

  function getNumberUnit (num) {
    var units = ["M","B","T"]
    var unit = Math.floor((num / 1.0e+1).toFixed(0).toString().length)
    var r = unit % 3
    var x =  Math.abs(Number(num))/Number('1.0e+'+(unit-r)).toFixed(2)
    return x.toFixed(2) + units[Math.floor(unit / 3) - 2]
  }

  return (
    <Container fluid>
      <div className="generalInfoContainer">
        {stock.companyName}
        <br/>
        {stock.symbol}
        <br/>
        {stock.pegRatio}
        <br/>
        {stock.divYield}
        <br/>
        {stock.marketCap}
      </div>
    </Container>
  );
}

export default Statistics