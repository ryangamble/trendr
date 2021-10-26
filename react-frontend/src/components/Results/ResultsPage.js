import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { useParams, Link } from "react-router-dom";
import MyNavBar from "../NavBar/MyNavBar";
import { SentimentGraph, StockGraph } from "./Graph";
import Statistics from "./Statistics";
import { Container, Col, Row, Button, Spinner } from "react-bootstrap";
import FollowBtn from "../FollowButton/FollowBtn";

function Results() {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  //current user
  const currentUser = useSelector((state) => state.user);

  const { id } = useParams();
  const [currency, setCurrency] = useState(null);
  const [isFollow, setIsFollow] = useState(false);

  const setCurrencyCallback = (curr) => {
    console.log("currency is " + curr);
    setCurrency(curr);
  };

  useEffect(() => {
    // do this only if user is logged in
    if (currentUser.email !== "" || currentUser.username !== "") {
      console.log("fetching user follow list");
      const list = ["DDOG", "APP"];
      // check if user follows this stock/crypto
      if (list.includes(id.substring(1))) {
        console.log("-----------------------");
        setIsFollow(true);
      }
    }
  }, []);

  return (
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
          <Col xs={12} className="resultsHeader">
            <h3 style={{ marginRight: 10 }}>
              Showing Results For: {id.substring(1)}
            </h3>
            {currentUser.username === "" && currentUser.email === "" ? null : (
              <FollowBtn id={id.substring(1)} isFollow={isFollow} />
            )}
          </Col>
        </Row>
        <Row>
          <Col xs={12} sm={12} md={12} lg={6}>
            <Statistics
              symbol={id.substring(1)}
              currencyCallback={setCurrencyCallback}
            />
            <br />
          </Col>
          <Col xs={12} sm={12} md={12} lg={6}>
            {currency ? (
              <StockGraph
                symbol={id.substring(1)}
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
              <StockGraph
                symbol={id.substring(1)}
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
          <Col xs={12} sm={12} md={12} lg={6}>
            <SentimentGraph symbol={id.substring(1)} />
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

export default Results;
