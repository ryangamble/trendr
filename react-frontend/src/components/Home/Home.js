import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import SearchBar from "../SearchBar/SearchBar";

import { useSelector } from "react-redux";
import FearGreed from "../FearGreed/FearGreed";
import {GdowGraph} from "./gdow";
import {BitcoinGraph} from "./bitcoin";
import {SP500Graph} from "./sp500";
import { Container, Col, Spinner } from "react-bootstrap";
import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";


function Home() {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  //current user
  const currentUser = useSelector((state) => state.user);

  const { id } = useParams();
  const [currency, setCurrency] = useState(null);

  const setCurrencyCallback = (curr) => {
    console.log("currency is " + curr);
    setCurrency(curr);
  };

  return (
    <div style={{ backgroundColor: currentTheme.background, height: "100vh" }}>
      <MyNavBar />
      <SearchBar />
      <FearGreed />
      <Col xs={12} sm={12} md={12} lg={6}>
            {currency ? (
              <GdowGraph
                symbol={"placeholder"}
                currency={'placeHolder'}
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
              <BitcoinGraph
                symbol={"placeholder"}
                currency={'placeHolder'}
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
              <SP500Graph
                symbol={"placeholder"}
                currency={'placeHolder'}
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
    </div>
  );
}

export default Home;