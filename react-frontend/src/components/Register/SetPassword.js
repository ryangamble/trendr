import React, { useState } from "react";
import { useHistory, useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import MyNavBar from "../NavBar/MyNavBar";
import { Row, Col, Form, Button, Card } from "react-bootstrap";
import axios from "axios";

function SetPassword() {
  const { resetCode } = useParams();
  const currentTheme = useSelector((state) => state.theme.currentTheme);
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
      password: password1,
      password_confirm: password2,
    });
    const config = {
      headers: { "Content-Type": "application/json" }
    };

    axios
      .post(
        "http://localhost:5000/auth/reset/" + resetCode.substring(1),
        json,
        config
      )
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
              Reset Your Password
            </Card.Header>
            <Card.Body>
              <Form onSubmit={handleSubmit}>
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
                  <Col sm="4">
                    <Button variant={currentTheme.variant} type="submit">
                      Set Password
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

export default SetPassword;
