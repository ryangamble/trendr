import React, { useEffect, useState } from "react";
import {Container, Image, ListGroup, Row, Col} from "react-bootstrap";
import axios from "axios";
import "./Results.css"

function Statistics(props) {
  
  const [stock, setStock] = useState([]);

  const requestBody = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json'},
    name: props.symbol
  }

  useEffect(() => {
    axios.post('/api/result/stats', requestBody)
      .then(res => {
        return JSON.parse(JSON.stringify(res.data));
      })
      .then (data => {
        setStock({
          companyName: data['longName'] ? data['longName'] : data['shortName'],
          logo: data['logo_url'],
          symbol: data['symbol'],
          dayOpen: data['open'].toFixed(2),
          dayHigh: data['dayHigh'].toFixed(2),
          dayLow: data['dayLow'].toFixed(2),
          fiftyTwoWeekHigh: data['fiftyTwoWeekHigh'].toFixed(2),
          fiftyTwoWeekLow: data['fiftyTwoWeekLow'].toFixed(2),
          volume: data['volume'],
          avgVolume: data['averageVolume'],
          marketCap: getNumberUnit(data['marketCap']),
          pegRatio: data['pegRatio'] ? (data['pegRatio']).toFixed(2) : "N/A",
          divYield: data['dividendYield'] ? (data['dividendYield'] * 100).toFixed(2) : "N/A"
        });

        console.log(data);
      })
      .catch((error) => {
        console.log(error);
      });
      
  }, []);

  function getNumberUnit (num) {
    var units = ["M", "B", "T", "Q"]
    var unit = Math.floor((num / 1.0e+1).toFixed(0).toString().length)
    var r = unit % 3
    var x =  Math.abs(Number(num)) / Number('1.0e+' + (unit - r)).toFixed(2)
    return x.toFixed(2) + units[Math.floor(unit / 3) - 2]
  }

  return (
    <Container fluid>
      <Row>
        <Image src={stock.logo} rounded/>
        <h2>{stock.companyName}</h2>
      </Row>
      <Row>
        <Col>
        <ListGroup variant="flush">
          <ListGroup.Item>Symbol: {stock.symbol}</ListGroup.Item>
          <ListGroup.Item>Day Open: {stock.dayOpen}</ListGroup.Item>
          <ListGroup.Item>Day High: {stock.dayHigh}</ListGroup.Item>
          <ListGroup.Item>Day Low: {stock.dayLow}</ListGroup.Item>
          <ListGroup.Item>52 Week High: {stock.fiftyTwoWeekHigh}</ListGroup.Item>
          <ListGroup.Item>52 Week Low: {stock.fiftyTwoWeekLow}</ListGroup.Item>
        </ListGroup>
        </Col>
        <Col>
        <ListGroup variant="flush">
          <ListGroup.Item>Volume: {stock.volume}</ListGroup.Item>
          <ListGroup.Item>Average Volume: {stock.avgVolume}</ListGroup.Item>
          <ListGroup.Item>52 Week High: {stock.fiftyTwoWeekHigh}</ListGroup.Item>
          <ListGroup.Item>Div/Yield: {stock.divYield}</ListGroup.Item>
          <ListGroup.Item>PEG ratio: {stock.pegRatio}</ListGroup.Item>
          <ListGroup.Item>Market Cap: {stock.marketCap}</ListGroup.Item>
        </ListGroup>
        </Col>
      </Row>
    </Container>
  );
}

export default Statistics