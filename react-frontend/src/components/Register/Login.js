import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { registerConfirmation, registerUser } from "../Theme/userActions";
import { toggleTheme, themes } from "../Theme/themeActions";
import MyNavBar from "../NavBar/MyNavBar";
import { Row, Col, Form, Button, Card } from "react-bootstrap";
import { Link } from "react-router-dom";
import axios from "axios";

import axios from 'axios'

function Login () {
  const currentTheme = useSelector((state) => state.theme.currentTheme)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const dispatch = useDispatch()
  const history = useHistory()

  const handleSubmit = (event) => {
    event.preventDefault()

    const json = JSON.stringify({
      email: email,
      password: password
    })
    const config = {
      headers: { 'Content-Type': 'application/json' },
      withCredentials: true
    }

    axios
      .post('http://localhost:5000/auth/login', json, config)
      .then((res) => {
        // register the user to global user
        dispatch(registerUser('', email))
        history.push('/home')
        // TODO: replace when we get better settings storage
        axios
          .get("http://localhost:5000/users/settings", {
            withCredentials: true,
          })
          .then((response) => {
            console.log("Read theme from user settings");
            console.log(
              "server: " +
                response.data.dark_mode +
                "\nclient: " +
                (currentTheme === themes.dark)
            );
            // false represents light, true represents dark
            if (
              (response.data.dark_mode === false &&
                currentTheme === themes.dark) ||
              (response.data.dark_mode === true &&
                currentTheme === themes.light)
            ) {
              dispatch(toggleTheme());
            }
          })
          .catch((err) => {
            console.log(err);
          });
      })
      .catch((error) => {
        // alert(JSON.stringify(error.response.data.response.errors));
        console.log(error.response.data.response.errors);
        //If the user hasn't confirmed email, we will redirect to confirmation page
        if (error.response.data.response.errors.email) {
          dispatch(registerConfirmation(email));
          history.push("/confirmation");
        }
      });
  };

  return (
    <div
      style={{
        background: currentTheme.background,
        color: currentTheme.foreground,
        height: '100vh'
      }}
    >
      <MyNavBar />
      <Row className="justify-content-md-center">
        <Col sm="12" md="6" lg="3">
          <Card>
            <Card.Header
              style={{ color: currentTheme.textColorLightBackground }}
            >
              Login
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
                    <Link
                      to="register"
                      style={{ color: currentTheme.linkColor }}
                    >
                      Register An Account{' '}
                    </Link>
                  </Col>
                  <Col sm="4">
                    <Link to="reset" style={{ color: currentTheme.linkColor }}>
                      Reset Password{' '}
                    </Link>
                  </Col>
                </Row>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Login
