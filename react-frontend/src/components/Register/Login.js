import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { useSelector } from "react-redux";
import MyNavBar from "../NavBar/MyNavBar";
import { Row, Col, Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import axios from "axios";

function Login() {
  const currentTheme = useSelector((state) => state.currentTheme);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const history = useHistory();

  const handleSubmit = (event) => {
    event.preventDefault();

    const json = JSON.stringify({
      "email": email,
      "password": password,
    });
    const config = {
      headers: { "Content-Type": "application/json" }
    };

    axios
        .post("http://localhost:5000/auth/login", json, config)
        .then((res) => {
          history.push("/home");
        })
        .catch((error) => {
          alert(error.response.data.response.errors);
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
      <Row className="position-relative">
        <h2>Log In To Your Account</h2>
      </Row>
      <Row className="justify-content-md-center">
        <Col sm="12" md="6">
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Form.Group>

            <Row className="justify-content-sm-center">
              <Col sm="4">
                <Button variant={currentTheme.variant} type="submit">
                  Log In
                </Button>
              </Col>
              <Col sm="4">
                <Link to="register" style={{ color: currentTheme.linkColor }}>
                  Register An Acocunt{" "}
                </Link>
              </Col>
              <Col sm="4">
                <Link to="reset" style={{ color: currentTheme.linkColor }}>
                  Reset Password{" "}
                </Link>
              </Col>
            </Row>
          </Form>
        </Col>
      </Row>
    </div>
  );
}

export default Login;
