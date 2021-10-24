import React, { useState, useEffect } from "react";
import MyNavBar from "../NavBar/MyNavBar";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import {
  Col,
  Container,
  ListGroup,
  Row,
  Badge,
  Button,
  ListGroupItem,
} from "react-bootstrap";
import "./MyAccount.css";
import FollowBtn from "../FollowButton/FollowBtn";

function MyAccount() {
  //color theme
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  //current user
  const currentUser = useSelector((state) => state.user);

  //List of followed stocks/cryptos
  const [list, setList] = useState([]);

  useEffect(() => {
    // get the user follow list
    if (currentUser.email !== "" || currentUser.username !== "") {
      console.log("profile fetching user follow list....");

      //set the list
      setList(["APP", "DDOG", "GH"]);
    }
  }, []);

  const unfollowCallback = (item) => {
    setList(list.filter((x) => x !== item));
  };

  return (
    <div
      style={{
        backgroundColor: currentTheme.background,
        height: "100vh",
        color: currentTheme.foreground,
      }}
      className="myAccountWrapper"
    >
      <MyNavBar />

      <Container>
        <Row align="left">
          <Col xs={12} md={3}>
            <h3>
              Welcome{" "}
              {currentUser.username === "" && currentUser.email === ""
                ? "Guest!"
                : currentUser.email}
            </h3>

            {currentUser.username === "" && currentUser.email === "" ? (
              <Link to="login">Login to see your profile</Link>
            ) : null}
          </Col>
        </Row>

        <br />
        <br />
        {currentUser.username === "" && currentUser.email === "" ? null : (
          <div>
            <Row>
              <Col xs={12} md={3}>
                <h3>
                  <Badge bg="info">Your Followed Cryptos/Stocks:</Badge>
                </h3>
              </Col>
            </Row>

            <Row>
              <Col xs={12}>
                <ListGroup variant="flush" align="left">
                  {list.map((item) => (
                    <ListGroupItem
                      variant={currentTheme.name.toLowerCase()}
                      action
                      href={`/result:${item}`}
                      key={item}
                    >
                      {item} <FollowBtn id={item} callback={unfollowCallback} />
                    </ListGroupItem>
                  ))}
                </ListGroup>
              </Col>
            </Row>
          </div>
        )}
      </Container>
    </div>
  );
}

export default MyAccount;
