import React, { useState } from "react";
import {useHistory, useParams} from "react-router-dom";
import { useSelector } from "react-redux";
import MyNavBar from "../NavBar/MyNavBar";
import { Row, Col, Form, Button } from "react-bootstrap";
import axios from "axios";

function SetPassword() {
    const { resetCode } = useParams();
    const currentTheme = useSelector((state) => state.currentTheme);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);
    const [password1, setPassword1] = useState("");
    const [password2, setPassword2] = useState("");

    const history = useHistory();

    const handleSubmit = (event) => {
        event.preventDefault();
        setSuccess(false)
        setError(false)

        if (password1 !== password2) {
            alert("Passwords are not the same!");
            setError(true)
            return;
        }

        console.log("firing set password request to the backend...");

        const json = JSON.stringify({
            "password": password1,
            "password_confirm": password2
        })
        const config = {
          headers: { "Content-Type": "application/json" }
        }

        axios
            .post("http://localhost:5000/auth/reset/" + resetCode, json, config)
            .then((res) => {
                if (res.status === 200) {
                    console.log("reset response:");
                    console.log(res.data);
                    setSuccess(true);
                    history.push("/home");
                }
            })
            .catch((error) => {
                console.log(error);
                console.log(error.response);
                setError(true)
                if (error.response.status === 400) {
                    alert(error.response.data.error);
                }
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
                <h2>Reset Your Password</h2>
            </Row>
            {error &&
                <Row>
                    <p>Error, could not set password.</p>
                </Row>
            }
            {success &&
                <Row>
                    <p>Password set.</p>
                </Row>
            }
            <Row className="justify-content-md-center">
                <Col sm="12" md="6">
                    <Form onSubmit={handleSubmit}>
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
                            <Col sm="4">
                                <Button variant={currentTheme.variant} type="submit">
                                    Set Password
                                </Button>
                            </Col>
                        </Row>
                    </Form>
                </Col>
            </Row>
        </div>
    );
}

export default SetPassword;
