import React, { useState, useEffect } from "react";
import MyNavBar from "../NavBar/MyNavBar";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { Col, Container, Row, Button, Alert } from "react-bootstrap";
import axios from "axios";

function ConfirmationPage() {
  //color theme
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  //current user
  const currentUser = useSelector((state) => state.user);

  const handleResend = () => {
    console.log("resending the Email...");
    const json = JSON.stringify({
      email: currentUser.tempEmail,
    });
    const config = {
      headers: { "Content-Type": "application/json" },
    };

    axios
      .post("http://localhost:5000/auth/confirm", json, config)
      .then((res) => {
        alert("We have resent confirmation successfully!");
      })
      .catch((error) => {
        alert(error);
      });
  };
  return (
    <div
      style={{
        backgroundColor: currentTheme.background,
        height: "100vh",
        color: currentTheme.foreground,
      }}
    >
      <MyNavBar />

      <Container style={{ marginTop: "10%" }}>
        <Row className="justify-content-center">
          <Col xs={6}>
            <Alert variant="info">
              A confirmation email has been sent to your email address:{" "}
              {currentUser.tempEmail}
            </Alert>
          </Col>

          <Col xs={12} align="center">
            <h5>Click here to resend the confirmation email:</h5>
            <Button variant={currentTheme.variant} onClick={handleResend}>
              Resend
            </Button>
            <br />
            <Link to="/login" style={{ color: currentTheme.linkColor }}>
              I have confirmed my email, return to login
            </Link>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default ConfirmationPage;
