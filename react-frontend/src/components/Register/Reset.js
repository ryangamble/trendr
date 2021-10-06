import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { useSelector } from "react-redux";
import MyNavBar from "../NavBar/MyNavBar";
import { Row, Col, Form, Button, Card } from "react-bootstrap";
import axios from "axios";

function Reset() {
    const currentTheme = useSelector((state) => state.currentTheme);
    const [email, setEmail] = useState("");
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);

    const history = useHistory();

    const handleSubmit = (event) => {
        event.preventDefault();
        setSuccess(false)
        setError(false)
        console.log("firing reset password request to the backend...");
        console.log("Email is ", email);

        const json = JSON.stringify({
            "email": email,
        })
        const config = {
            headers: { "Content-Type": "application/json" }
        }

        axios
            .post("http://localhost:5000/auth/reset", json, config)
            .then((res) => {
                setSuccess(true);
            })
            .catch((error) => {
                setError(true)
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
            {error &&
                <Row>
                    <p>Error, could not reset password.</p>
                </Row>
            }
            {success &&
                <Row>
                    <p>Password reset request sent.</p>
                </Row>
            }
            <Row className="justify-content-md-center">
                <Col sm="12" md="6" lg="3">
                    <Card>
                        <Card.Header>Reset Your Password</Card.Header>
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
