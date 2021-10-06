import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import { useSelector } from "react-redux";
import {Container, Card, Row, Col} from "react-bootstrap";

function Home() {
  const currentTheme = useSelector((state) => state.currentTheme);

  return (
    <div
      style={{
        background: currentTheme.background,
        color: currentTheme.foreground,
        height: "100vh",
      }}
    >
      <MyNavBar/>
      <Container>
        <div style={{justifyContent:"left"}}>
          <h1>Welcome to Trendr</h1>
        </div>
        <br/>
        <Row>
          <Col>
            <Card bg={currentTheme.variant} text="white">
              <Card.Body>
                <Card.Title>
                  Stock and Crypto Data
                </Card.Title>
                <Card.Text>
                  Search for any stock or crypto and get the basic financial statistics, 
                  alongside a price and volume history charts.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <br/>
          <Col>
            <Card bg={currentTheme.variant} text="white">
              <Card.Body>
                <Card.Title>
                  Create an account
                </Card.Title>
                <Card.Text>
                  Create an account on this platform to save your searches and
                  to access any premium features
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>
        <br/>
        <Row style={{margin:"0.5rem"}}>
          <Card bg={currentTheme.variant} text="white">
            <Card.Body>
              <Card.Title>
                Sentiment Analysis
              </Card.Title>
              <Card.Text>
                For any given stock/crypto, our website performs 
                sentiment analysis on Tweets and Reddit posts on the stock/crypto.
              </Card.Text>
            </Card.Body>
          </Card>
        </Row>
        <br/>
      </Container>
    </div>
  );
}

export default Home;
