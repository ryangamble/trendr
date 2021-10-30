import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { useParams, Link } from "react-router-dom";
import MyNavBar from "../NavBar/MyNavBar";
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
import { Container, Col, Row, Button, Spinner } from "react-bootstrap";
import FollowBtn from "../FollowButton/FollowBtn";


function Results(props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  //current user
  const currentUser = useSelector((state) => state.user);

  const { id, type } = useParams();
  const [currency, setCurrency] = useState(null);
  const [tokenAddr, setTokenAddr] = useState(null);

  const setCurrencyCallback = (curr) => {
    setCurrency(curr);
  };

  const setTokenAddrCallback = (addr) => {
    console.log("token address is " + addr)
    setTokenAddr(addr);
  }

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
            <Col xs={12} className="resultsHeader">
              <h3 style={{ marginRight: 10 }}>
                Showing Results For: {id}
              </h3>
              {currentUser.username === "" && currentUser.email === "" ? null : (
                <FollowBtn id={id} />
              )}
            </Col>
          </Row>
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
              <Col xs={12} sm={12} md={12} lg={6}>
                <CoinStatistics
                  id={id}
                  addrCallback={setTokenAddrCallback}
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
                {tokenAddr == "none" ? (
                  null
                ) : (tokenAddr == null ? (
                  <Container fluid>
                    <Spinner animation="border" />
                  </Container>
                ) : (
                  <TokenStatistics addr={tokenAddr}/>
                )
                )}
                <br/>
              </Col>
              <Col xs={12} sm={12} md={12} lg={6}>
                {tokenAddr == "none" ? (
                  null
                ) : (tokenAddr == null ? (
                  <Container fluid>
                    <Spinner animation="border" />
                  </Container>
                ) : (
                  <TopTokenHolders addr={tokenAddr}/>
                )
                )}
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
}

export default Results;