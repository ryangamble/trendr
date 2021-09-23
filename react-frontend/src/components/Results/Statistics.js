import React, { useEffect, useState } from "react";
import {Container, Image, Table, Col, Spinner} from "react-bootstrap";
import axios from "axios";
import "./Results.css"

function Statistics(props) {
  
  const [stock, setStock] = useState([]);
  const [loading, setLoading] = useState(true);

  const requestBody = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json'},
    name: props.symbol
  }

  useEffect(() => {
    setLoading(true);
    axios.post('/api/result/stats', requestBody)
      .then(res => {
        setLoading(true);
        return JSON.parse(JSON.stringify(res.data));
      })
      .then (data => {
        setStock({
          companyName: data['longName'] ? data['longName'] : data['shortName'],
          logo: data['logo_url'],
          symbol: data['symbol'],
          dayOpen: formatPrice(data['open']),
          dayHigh: formatPrice(data['dayHigh']),
          dayLow: formatPrice(data['dayLow']),
          fiftyTwoWeekHigh: formatPrice(data['fiftyTwoWeekHigh']),
          fiftyTwoWeekLow: formatPrice(data['fiftyTwoWeekLow']),
          volume: data['volume'].toLocaleString("en-US"),
          avgVolume: data['averageVolume'].toLocaleString("en-US"),
          marketCap: '$' + getNumberUnit(data['marketCap']),
          pegRatio: data['pegRatio'] ? (data['pegRatio']).toFixed(2) : "N/A",
          divYield: data['dividendYield'] ? (data['dividendYield'] * 100).toFixed(2) : "N/A"
        });

        console.log(data);
      })
      .then (() => {
        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
      });
      
  }, [props]);

  function formatPrice (num) {
    const options = {
      style: 'currency',
      currency: 'USD'
    };
    return num.toLocaleString("en-US", options);
  }

  function getNumberUnit (num) {
    var units = ["M", "B", "T", "Q"]
    var unit = Math.floor((num / 1.0e+1).toFixed(0).toString().length)
    var r = unit % 3
    var x =  Math.abs(Number(num)) / Number('1.0e+' + (unit - r)).toFixed(2)
    return x.toFixed(2) + units[Math.floor(unit / 3) - 2]
  }

  if (loading) {
    return (
      <Container fluid>
        <Spinner animation="border"/>  
      </Container>
    );
  } else {
    return (
      <Container fluid>
        <Col>
          <Image src={stock.logo} rounded/>
          <h2>{stock.companyName}</h2>
          <p>{stock.symbol}</p>
        </Col>
        <Col>
          <Table hover size="sm">
            <tbody>
              <tr>
                <td className="statName">Day Open</td>
                <td className="statValue">{stock.dayOpen}</td>
              </tr>
              <tr>
                <td className="statName">Day High</td>
                <td className="statValue">{stock.dayHigh}</td>
              </tr>
              <tr>
                <td className="statName">Day Low</td>
                <td className="statValue">{stock.dayLow}</td>
              </tr>
              <tr>
                <td className="statName">52 Week High</td>
                <td className="statValue">{stock.fiftyTwoWeekHigh}</td>
              </tr>
              <tr>
                <td className="statName">52 Week Low</td>
                <td className="statValue">{stock.fiftyTwoWeekLow}</td>
              </tr>
              <tr>
                <td className="statName">Volume</td>
                <td className="statValue">{stock.volume}</td>
              </tr>
              <tr>
                <td className="statName">Avg. Volume</td>
                <td className="statValue">{stock.avgVolume}</td>
              </tr>
              <tr>
                <td className="statName">Div/Yield</td>
                <td className="statValue">{stock.divYield}</td>
              </tr>
              <tr>
                <td className="statName">PEG ratio</td>
                <td className="statValue">{stock.pegRatio}</td>
              </tr>
              <tr>
                <td className="statName">Market Cap</td>
                <td className="statValue">{stock.marketCap}</td>
              </tr>
            </tbody>        
          </Table>
        </Col>
      </Container>
    );
  }
}

export default Statistics