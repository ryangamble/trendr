import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { useSelector } from "react-redux";
import MyNavBar from "../NavBar/MyNavBar";
import { Row, Col, Form, Button } from "react-bootstrap";
import axios from "axios";

function Login() {
    const currentTheme = useSelector((state) => state.currentTheme);
    const [email, setEmail] = useState("");
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);
    const [csrfToken, setCsrfToken] = useState("");

    const history = useHistory();

    const handleSubmit = (event) => {
        event.preventDefault();
        setSuccess(false)
        setError(false)
        console.log("firing reset password request to the backend...");
        console.log("Email is ", email);

        const tokenRequestBody = {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            data: null,
        };

        const resetRequestBody = {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken},
            data: {"email": email},
        };

        axios
            .get("/auth/reset", tokenRequestBody)
            .then((res) => {
                if (res.status === 200) {
                    setCsrfToken(res.data['response']['csrf_token']);
                    console.log("token response:");
                    console.log(res.data);
                    axios
                        .post("/auth/reset", resetRequestBody)
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
                    <p>Error, could not reset password.</p>
                </Row>
            }
            {success &&
                <Row>
                    <p>Password reset request sent.</p>
                </Row>
            }
            <Row className="justify-content-md-center">
                <Col sm="12" md="6">
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
                </Col>
            </Row>
        </div>
    );
}

export default Login;
