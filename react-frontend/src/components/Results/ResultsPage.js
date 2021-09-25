import React from "react";
import {useParams} from "react-router-dom";
import MyNavBar from "../NavBar/MyNavBar";
import PriceChart from "./PriceChart";
import Statistics from "./Statistics";
import {Container, Col, Row, Button} from "react-bootstrap";

function Results() {

  const {id} = useParams();

  return (
    <div className="resultsPage">
      <MyNavBar/>
      <br/>
      <br/>
      <Container>
        <Row>
          <Col xs={12} sm={12} md={12} lg={6}>
            <Statistics symbol={id.substring(1)}/>
            <br/>
          </Col>
          <Col xs={12} sm={12} md={12} lg={6}>
            <PriceChart symbol={id.substring(1)}/>
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