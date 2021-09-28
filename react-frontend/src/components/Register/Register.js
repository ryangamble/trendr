import React, { useState } from "react";
import { Form, Button, Col, Row } from "react-bootstrap";
import MyNavBar from "../NavBar/MyNavBar";
import { Link } from "react-router-dom";

function Register() {
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("firing registration request to the backend...");
    console.log("Email is ", email);
    console.log("password1 is ", password1);
    console.log("password2 is ", password2);

    if (password1 !== password2) {
      alert("Passwords are not the same!");
      return;
    }
  };
  return (
    <div>
      <MyNavBar />
      <Row className="position-relative">
        <h2>Register an account</h2>
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
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Password"
                value={password1}
                onChange={(e) => setPassword1(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Retype password"
                value={password2}
                onChange={(e) => setPassword2(e.target.value)}
                required
              />
            </Form.Group>

            <Row className="justify-content-sm-center">
              <Col sm="6">
                <Button variant="primary" type="submit">
                  Register
                </Button>
              </Col>
              <Col sm="6">
                <Link to="login">Already have an account? Login</Link>
              </Col>
            </Row>
          </Form>
        </Col>
      </Row>
    </div>
  );
}

export default Register;
