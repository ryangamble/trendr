import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import SearchBar from "../SearchBar/SearchBar";

import { useSelector } from "react-redux";
import FearGreed from "../FearGreed/FearGreed";
import {StockGraph} from "./CustomGraph";
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
              <StockGraph
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