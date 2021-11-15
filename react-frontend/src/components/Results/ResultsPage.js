import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { useParams, Link } from "react-router-dom";
import MyNavBar from "../NavBar/MyNavBar";
import TweetSummary from "./TweetSummary";
import { Container, Col, Row, Spinner } from "react-bootstrap";
import {
  SentimentGraph,
  StockGraph,
  CryptoGraph,
  TopTokenHolders,
} from "./Graph";
import { StockStatistics, CoinStatistics, TokenStatistics } from "./Statistics";
import FollowBtn from "../FollowButton/FollowBtn";
import axios from "axios";

function Results(props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  //current user
  const currentUser = useSelector((state) => state.user);

  const { id } = useParams();
  const [currency, setCurrency] = useState(null);
  const [isFollow, setIsFollow] = useState(false);
  const [type, setType] = useState(null);
  const [symbol, setSymbol] = useState(null);
  const [addr, setAddr] = useState(null);

  const setCurrencyCallback = (curr) => {
    setCurrency(curr);
  };

  useEffect(() => {
    console.log("id is", id);
    console.log(id.substring(0, id.indexOf(":")));
    setType(id.substring(0, id.indexOf(":")));
    if (id.lastIndexOf(":") != id.indexOf(":")) {
      setAddr(id.substring(id.lastIndexOf(":") + 1));
      setSymbol(id.substring(id.indexOf(":") + 1, id.lastIndexOf(":")));
    } else {
      setSymbol(id.substring(id.indexOf(":") + 1));
      console.log(id.substring(id.indexOf(":") + 1));
    }
  });

  useEffect(() => {
    // do this only if user is logged in
    if (currentUser.email !== "" || currentUser.username !== "") {
      console.log("fetching user follow list");

      axios
        .get(`http://localhost:5000/users/assets-followed`, {
          withCredentials: true,
        })
        .then((res) => {
          return res.data;
        })
        .then((data) => {
          console.log(data);
          console.log(data["assets"], id);
          if (data["assets"].includes(id)) {
            setIsFollow(true);
            console.log("yes", props.location, props.location.state);
          }
        })
        .catch((error) => {
          alert(JSON.stringify(error.response.data.response.errors));
        });
    }
  }, []);

  if (type && symbol) {
    if (type === "crypto") {
      return renderCryptoResults();
    } else {
      return renderStockResults();
    }
  } else {
    return null;
  }

  function renderStockResults() {
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
              <h3 style={{ marginRight: 10 }}>Showing Results For: {symbol}</h3>
              {currentUser.username === "" &&
              currentUser.email === "" ? null : (
                <FollowBtn id={id} isFollow={isFollow} />
              )}
            </Col>
          </Row>
          <br />
          <Row>
            <Col xs={12} sm={12} md={12} lg={6}>
              <StockStatistics
                symbol={symbol}
                currencyCallback={setCurrencyCallback}
              />
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              {currency ? (
                <StockGraph
                  symbol={symbol}
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
                <StockGraph symbol={symbol} graphType="volume" color="orange" />
              ) : (
                <Container fluid>
                  <Spinner animation="border" />
                </Container>
              )}
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              <SentimentGraph symbol={symbol} />
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              <TweetSummary symbol={symbol} />
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
              <h3 style={{ marginRight: 10 }}>Showing Results For: {symbol}</h3>
              {currentUser.username === "" &&
              currentUser.email === "" ? null : (
                <FollowBtn id={id} isFollow={isFollow} />
              )}
            </Col>
          </Row>
          <br />
          <Row>
            <Col xs={12} sm={12} md={12} lg={6}>
              <CoinStatistics id={symbol} />
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              <CryptoGraph symbol={symbol} graphType="price" color="#0D6EFD" />
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              <CryptoGraph symbol={symbol} graphType="volume" color="orange" />
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              {addr && <TokenStatistics addr={addr} />}
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              {addr && <TopTokenHolders addr={addr} />}
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              <SentimentGraph symbol={symbol} />
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              <TweetSummary symbol={symbol} />
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
