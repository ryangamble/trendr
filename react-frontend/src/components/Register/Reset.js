import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { useSelector } from "react-redux";
import MyNavBar from "../NavBar/MyNavBar";
import { Row, Col, Form, Button, Card } from "react-bootstrap";
import axios from "axios";

function Reset() {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  const [email, setEmail] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    setSuccess(false);

    const json = JSON.stringify({
      email: email,
    });
    const config = {
      headers: { "Content-Type": "application/json" },
      withCredentials: true,
    };

    axios
      .post("http://localhost:5000/auth/reset", json, config)
      .then((res) => {
        setSuccess(true);
      })
      .catch((error) => {
        alert(JSON.stringify(error.response.data.response.errors));
      });
  };

  return (
    <div
      style={{
        background: currentTheme.background,
        color: currentTheme.foreground,
        height: "100vh",
      }}
    >
      <MyNavBar />
      {success && (
        <Row>
          <p>Password reset request sent.</p>
        </Row>
      )}
      <Row className="justify-content-md-center">
        <Col sm="12" md="6" lg="3">
          <Card>
            <Card.Header
              style={{ color: currentTheme.textColorLightBackground }}
            >
              Reset Your Password
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                  <Form.Control
                    type="email"
                    placeholder="Enter email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </Form.Group>

                <Row className="justify-content-sm-center">
                  <Col sm="4">
                    <Button variant={currentTheme.variant} type="submit">
                      Reset
                    </Button>
                  </Col>
                </Row>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default Reset;
