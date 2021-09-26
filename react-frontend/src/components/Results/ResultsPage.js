import React, {useState} from "react";
import {useParams} from "react-router-dom";
import MyNavBar from "../NavBar/MyNavBar";
import Graph from "./Graph";
import Statistics from "./Statistics";
import {Container, Col, Row, Button, Spinner} from "react-bootstrap";

function Results() {

  const {id} = useParams();
  const [currency, setCurrency] = useState(null);
 
  const setCurrencyCallback = (curr) => {
    console.log("currency is " + curr);
    setCurrency(curr);
  }

  return (
    <div className="resultsPage">
      <MyNavBar/>
      <br/>
      <br/>
      <Container className="resultsContainer">
        <Row>
          <Col xs={12} sm={12} md={12} lg={6}>
            <Statistics symbol={id.substring(1)} currencyCallback={setCurrencyCallback}/>
            <br/>
          </Col>
          <Col xs={12} sm={12} md={12} lg={6}>
            {currency ? <Graph symbol={id.substring(1)} currency={currency} graphType="price" color="#0D6EFD"/>
            :
            <Container fluid>
              <Spinner animation="border"/>
            </Container>
            }
            <br/>
          </Col>
          <Col xs={12} sm={12} md={12} lg={6}>
            {currency ? <Graph symbol={id.substring(1)} graphType="volume" color="orange"/>
            :
            <Container fluid>
              <Spinner animation="border"/>
            </Container>
            }
            <br/>
          </Col>
        </Row>
        <Button className="homeButton" href="home" size="sm">
          Return to Home
        </Button>
      </Container>
    </div>
  );
}

export default Results;