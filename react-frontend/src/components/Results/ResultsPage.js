import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import PriceChart from "./PriceChart";
import Statistics from "./Statistics";
import {Container, Col, Row} from "react-bootstrap";

function Results() {
  return (
    <div className="resultsPage">
      <MyNavBar/>
      <Container>
        <Row>
        <Col xs={12} sm={12} md={12} lg={6}>
          <Statistics symbol="MSFT"/>
          <br/>
        </Col>
        <Col xs={12} sm={12} md={12} lg={6}>
          <PriceChart symbol="MSFT"/>
          <br/>
        </Col>
        </Row>
      </Container>
    </div>
  );
}

export default Results;