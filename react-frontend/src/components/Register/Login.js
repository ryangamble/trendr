import React, { useState } from "react";
import MyNavBar from "../NavBar/MyNavBar";
import { Row, Col, Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("firing registration request to the backend...");
    console.log("Email is ", email);
    console.log("password1 is ", password);
  };
  return (
    <div>
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
              <Col sm="6">
                <Button variant="primary" type="submit">
                  Log In
                </Button>
              </Col>
              <Col sm="6">
                <Link to="register">Do not have an account? Register Now</Link>
              </Col>
            </Row>
          </Form>
        </Col>
      </Row>
    </div>
  );
}

export default Login;
