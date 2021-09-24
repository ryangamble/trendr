import React, {useEffect, useState, componentDidMount} from "react";
import {Container, Spinner, Row, Col, ButtonGroup, Button} from "react-bootstrap";
import {
  XAxis,
  YAxis,
  HorizontalGridLines,
  VerticalGridLines,
  FlexibleXYPlot,
  LineSeries,
  Crosshair,
  Borders
} from "react-vis";
import axios from "axios";
import "./Results.css";
import '../../../node_modules/react-vis/dist/style.css';

// Currently pass symbol as a prop, can be changed later
function PriceChart (props) {

  const [priceData, setPriceData] = useState([]);

  const [min, setMin] = useState(0);
  const [max, setMax] = useState(0);
  const [loadedCount, setLoadedCount] = useState(0);
  const [crosshairValues, setCrosshairValues] = useState([]);
  const [period, setPeriod] = useState('1d');

  const periodDisplay = {
    "1d": "Past Day",
    "5d": "Past 5 Days",
    "1mo": "Past Month",
    "3mo": "Past 3 Months",
    "1y": "Past Year"
  }

  useEffect(() => {
    setLoadedCount(0);
    for (var key in periodDisplay) {
      fetchDataPoints(key);
    }
    getMinMax();
  }, [props]);

  useEffect (() => {
    getMinMax();
  }, [period]);

  async function fetchDataPoints (timePeriod) {

    const requestBody = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      name: props.symbol,
      period: timePeriod
    }

    axios.post('/api/result/history', requestBody)
    .then(res => {
      return JSON.parse(JSON.stringify(res.data));
    })
    .then(data => {
      var pd = [];
      for (var key in data['Close']) {
        // console.log(key)
        // console.log(data['Close'][key].toFixed(2))
        var value = data['Close'][key].toFixed(2);
        pd.push({
          x: new Date(parseInt(key)),
          y: value
        });
      }
      return pd;
    })
    .then(pd => {
      switch (timePeriod) {
        case "1d": setPriceData(prev => ({...prev, "1d": pd}));
          break;
        case "5d": setPriceData(prev => ({...prev, "5d": pd}));
          break;
        case "1mo": setPriceData(prev => ({...prev, "1mo": pd}));
          break;
        case "3mo": setPriceData(prev => ({...prev, "3mo": pd}));
          break;
        case "1y": setPriceData(prev => ({...prev, "1y": pd}));
          break;
        default: setPriceData(prev => ({...prev, "1d": pd}));
      }
    })
    .then(() => {
      setPeriod(period);
      setLoadedCount(prevCount => prevCount + 1);
    })
  }

  function getMinMax () {
    var min = Number.MAX_VALUE;
    var max = 0;
    for (var key in priceData[period]) {
      var val = priceData[period][key].y
      if (val > max) {
        max = val;
      }
      if (val < min) {
        min = val;
      }
    }
    setMin(min);
    setMax(max);
  }

  function formatPrice (num) {
    const options = {
      style: 'currency',
      currency: 'USD'
    };
    return num.toLocaleString("en-US", options);
  }

  const _onMouseLeave = () => {
    setCrosshairValues([]);
  };

  const _onNearestX = (value) => {
    var x = new String(value.x)
    value.x = x;
    setCrosshairValues([value]);
  };

  const _itemsFormat = (data) => {
    return [{title: 'price', value: '$' + data[0].y}];
  }

  
  if (loadedCount < 5) {
    return (
      <Container fluid>
        <Spinner animation="border"/>  
      </Container>
    );
  } else {
    return (
      <Container className="graphLayout">
        <Row>
          <div className="chartTitle">
            <h2>Price history for {props.symbol}</h2>
          </div>
        </Row>
        <Row>
          <div className="chartContainer">
            <FlexibleXYPlot
              onMouseLeave={_onMouseLeave}
              xType="ordinal"
              yDomain={[0.98 * min, 1.02 * max]}
              >
              
              <HorizontalGridLines/>
              {/* <VerticalGridLines/> */}
            
              <LineSeries
                data={priceData[period]}
                onNearestX={_onNearestX}
                strokeWidth={2}
                opacity={1}
                color="#0D6EFD"
              />
              <Borders style={{
                bottom: {fill: '#fff'},
                left: {fill: '#fff'},
                right: {fill: '#fff'},
                top: {fill: '#fff'}
              }}/>
              
              <YAxis/>
              <XAxis
                hideTicks
              />

              <Crosshair
                values={crosshairValues}
                itemsFormat={_itemsFormat}
                
              />
              
            </FlexibleXYPlot>
          </div>
        </Row>
        <Row>
          <Col>
            <ButtonGroup size="sm">
              <Button
                variant="secondary"
                onClick={() => {setPeriod("1d")}}
                >
                  1D
              </Button>
              <Button
                variant="secondary"
                onClick={() => setPeriod("5d")}
              >
                5D
              </Button>
              <Button
                variant="secondary"
                onClick={() => setPeriod("1mo")}
              >
                1M
              </Button>
              <Button
                variant="secondary"
                onClick={() => setPeriod("3mo")}
              >
                3M
              </Button>
              <Button
                variant="secondary"
                onClick={() => setPeriod("1y")}
              >
                1Y
              </Button>
            </ButtonGroup>
          </Col>
          <Col>
            {priceData[period][(priceData[period].length - 1)].y - priceData[period][0].y > 0 ?
              <div className="priceUp">
                Up {formatPrice(priceData[period][priceData[period].length - 1].y - priceData[period][0].y)} {periodDisplay[period]}
              </div>
              :
              <div className="priceDown">
                Down {formatPrice(priceData[period][priceData[period].length - 1].y - priceData[period][0].y)} {periodDisplay[period]}
              </div>
            }
          </Col>
        </Row>

        
      </Container>
    );
  }
}

export default PriceChart;