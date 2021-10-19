import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { useParams, Link } from "react-router-dom";
import MyNavBar from "../NavBar/MyNavBar";
import Graph from "./Graph";
import Statistics from "./Statistics";
import { Container, Col, Row, Button, Spinner } from "react-bootstrap";
import FollowBtn from "../FollowButton/FollowBtn";

function Results() {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  //current user
  const currentUser = useSelector((state) => state.user);

  const { id, type } = useParams();
  const [currency, setCurrency] = useState(null);

  const setCurrencyCallback = (curr) => {
    console.log("currency is " + curr);
    setCurrency(curr);
  };

  if (type == "crypto") {
    return renderCryptoResults()
  } else {
    return renderStockResults()
  }


  function renderStockResults() {
    return(
      <div
        className="resultsPage"
        style={{
          background: currentTheme.background,
          color: currentTheme.foreground,
        }}
      >
        <MyNavBar />
        <br />
        <br />
        <Container className="resultsContainer">
          <Row>
            <Col xs={12} sm={12} md={12} lg={6}>
              <Statistics
                symbol={id}
                currencyCallback={setCurrencyCallback}
              />
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              {currency ? (
                <Graph
                  symbol={id}
                  currency={currency}
                  graphType="price"
                  color="#0D6EFD"
                />
              ) : (
                <Container fluid>
                  <Spinner animation="border" />
                </Container>
              )}
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              {currency ? (
                <Graph
                  symbol={id}
                  graphType="volume"
                  color="orange"
                />
              ) : (
                <Container fluid>
                  <Spinner animation="border" />
                </Container>
              )}
              <br />
            </Col>
          </Row>
          <Link to="home" style={{ color: currentTheme.linkColor }}>
            Return to Home
          </Link>
        </Container>
      </div>
    );
  }

  function renderCryptoResults() {
    return(
      <div>hello</div>
    );
  }
}

export default Results;
