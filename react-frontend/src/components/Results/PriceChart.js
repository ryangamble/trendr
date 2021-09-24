import React, {useEffect, useState} from "react";
import {Container, Spinner, Row, Col} from "react-bootstrap";
import {
  XAxis,
  YAxis,
  HorizontalGridLines,
  FlexibleXYPlot,
  LineSeries,
  Highlight,
  VerticalGridLines
} from "react-vis";
import axios from "axios";
import "./Results.css";
import '../../../node_modules/react-vis/dist/style.css';

// Currently pass symbol as a prop, can be changed later
function PriceChart(props) {

  const [priceData, setPriceData] = useState([]);
  const [lastLocation, setLastLocation] = useState(null);
  const [loading, setLoading] = useState(true);

  const requestBody = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json'},
    name: "MSFT"
  }

  useEffect(() => {
    setLoading(true);
    axios.post('/api/result/history', requestBody)
    .then(res => {
      return JSON.parse(JSON.stringify(res.data));
    })
    .then(data => {
      var pd = [];
      for (var key in data['Close']) {
        // console.log(key)
        // console.log(data['Close'][key].toFixed(2))
        pd.push({
          x: new Date(key * 1000),
          y: data['Close'][key].toFixed(2)
        });
      }
      return pd;
    })
    .then(pd => {
      setPriceData(pd);
      console.log(pd);
    })
    .then(() => {
      setLoading(false);
    })
  }, []);

  if (loading) {
    return (
      <Container fluid>
        <Spinner animation="border"/>  
      </Container>
    );
  } else {
    return(
      <Container fluid>
        <Row>
          <div>
            <h2>Price chart:</h2>
          </div>
        </Row>
        <Row>
          <div className="chartContainer">
            <FlexibleXYPlot
              animation
              xType="time"
              
              xDomain={
                lastLocation && [
                  lastLocation.left,
                  lastLocation.right
                ]
              }
              yDomain={
                lastLocation && [
                  lastLocation.bottom,
                  lastLocation.top
                ]
              }
              height={300}
              width={400}
              >
              <HorizontalGridLines />
              <VerticalGridLines />

              <YAxis title="price"/>
              <XAxis title="time"/>

              <LineSeries
                data={priceData}
                strokeWidth={2}
                opacity={1}
                color="#0D6EFD"
              />
              <Highlight
                onBrushEnd={area => setLastLocation(area)}
                onDrag={area => {
                  setLastLocation({
                    bottom: lastLocation.bottom + (area.top - area.bottom),
                    left: lastLocation.left - (area.right - area.left),
                    right: lastLocation.right - (area.right - area.left),
                    top: lastLocation.top + (area.top - area.bottom)
                  });
                }}
              />
            </FlexibleXYPlot>
          </div>
        </Row>
      </Container>
    );
  }
}

export default PriceChart;