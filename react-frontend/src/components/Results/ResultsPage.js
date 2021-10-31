import React, { useState } from "react";
import { useSelector } from "react-redux";
import { useParams, Link } from "react-router-dom";
import MyNavBar from "../NavBar/MyNavBar";
import TweetSummary from "./TweetSummary";
import { Container, Col, Row, Spinner } from "react-bootstrap";
import {
  SentimentGraph,
  StockGraph,
  CryptoGraph,
  TopTokenHolders} from "./Graph";
import {
  StockStatistics,
  CoinStatistics,
  TokenStatistics,
} from "./Statistics";
import FollowBtn from "../FollowButton/FollowBtn";


function Results(props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  //current user
  const currentUser = useSelector((state) => state.user);

  const { id, type } = useParams();
  const [currency, setCurrency] = useState(null);

  const setCurrencyCallback = (curr) => {
    setCurrency(curr);
  };

  if (type === "crypto") {
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
            <Col xs={12} className="resultsHeader">
              <h3 style={{ marginRight: 10 }}>
                Showing Results For: {props.location.state.symbol}
              </h3>
              {currentUser.username === "" && currentUser.email === "" ? null : (
                <FollowBtn id={id} />
              )}
            </Col>
          </Row>
          <br />
          <Row>
            <Col xs={12} sm={12} md={12} lg={6}>
              <StockStatistics
                symbol={id}
                currencyCallback={setCurrencyCallback}
              />
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              {currency ? (
                <StockGraph
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
                <StockGraph
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
            <Col xs={12} sm={12} md={12} lg={6}>
              <SentimentGraph symbol={id}/>
              <br/>
            </Col>
          </Row>
          <Link to="../../home" style={{ color: currentTheme.linkColor }}>
            Return to Home
          </Link>
        </Container>
      </div>
    );
  }

  function renderCryptoResults() {
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
              <Col xs={12} className="resultsHeader">
                <h3 style={{ marginRight: 10 }}>
                  Showing Results For: {props.location.state.symbol}
                </h3>
                {currentUser.username === "" && currentUser.email === "" ? null : (
                  <FollowBtn id={id} />
                )}
              </Col>
            </Row>
            <br />
            <Row>
              <Col xs={12} sm={12} md={12} lg={6}>
                <CoinStatistics
                  id={id}
                />
                <br />
              </Col>
              <Col xs={12} sm={12} md={12} lg={6}>
                <CryptoGraph
                  symbol={id}
                  graphType="price"
                  color="#0D6EFD"
                />
                <br />
              </Col>
              <Col xs={12} sm={12} md={12} lg={6}>
                <CryptoGraph
                  symbol={id}
                  graphType="volume"
                  color="orange"
                />
                <br />
              </Col>
              <Col xs={12} sm={12} md={12} lg={6}>
                {props.location.state.addr &&
                  <TokenStatistics addr={props.location.state.addr}/>
                }
                <br/>
              </Col>
              <Col xs={12} sm={12} md={12} lg={6}>
                {props.location.state.addr &&
                  <TopTokenHolders addr={props.location.state.addr}/>
                }
                <br/>
              </Col>
              <Col xs={12} sm={12} md={12} lg={6}>
                <SentimentGraph symbol={id}/>
                <br/>
              </Col>
              <Col xs={12} sm={12} md={12} lg={6}>
                <TweetSummary symbol={id.substring(1)}/>
                <br />
              </Col>
            </Row>
            <Link to="../../home" style={{ color: currentTheme.linkColor }}>
              Return to Home
            </Link>
          </Container>
      </div>
    );
  }
}

export default Results;
