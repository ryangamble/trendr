import React, { useState } from "react";
import { Form, Button, Col, Row, Card } from "react-bootstrap";
import { useHistory } from "react-router-dom";
import MyNavBar from "../NavBar/MyNavBar";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import axios from "axios";

function Register() {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");

  const history = useHistory();

  const handleSubmit = (event) => {
    event.preventDefault();

    if (password1 !== password2) {
      alert("Passwords are not the same!");
      return;
    }

    const json = JSON.stringify({
      email: email,
      password: password1,
    });
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    axios
      .post("http://localhost:5000/auth/register", json, config)
      .then((res) => {
        history.push("/login");
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
      <Row className="justify-content-md-center">
        <Col sm="12" md="6" lg="3">
          <Card>
            <Card.Header
              style={{ color: currentTheme.textColorLightBackground }}
            >
              Register
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                  <Form.Label
                    style={{ color: currentTheme.textColorLightBackground }}
                  >
                    Email address
                  </Form.Label>
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

                <Form.Group className="mb-3" controlId="formBasicUsername">
                  <Form.Label
                    style={{ color: currentTheme.textColorLightBackground }}
                  >
                    Username
                  </Form.Label>
                  <Form.Control
                    type="input"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicPassword">
                  <Form.Label
                    style={{ color: currentTheme.textColorLightBackground }}
                  >
                    Password
                  </Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Password"
                    value={password1}
                    onChange={(e) => setPassword1(e.target.value)}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicPassword">
                  <Form.Label
                    style={{ color: currentTheme.textColorLightBackground }}
                  >
                    Confirm Password
                  </Form.Label>
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
                    <Button variant={currentTheme.variant} type="submit">
                      Register
                    </Button>
                  </Col>
                  <Col sm="6">
                    <Link to="login" style={{ color: currentTheme.linkColor }}>
                      Already have an account? Login
                    </Link>
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

export default Register;
