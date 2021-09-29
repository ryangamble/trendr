import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { toggleTheme } from "../Theme/themeActions";
import { Navbar, Container, Nav, Button } from "react-bootstrap";
import { Link } from "react-router-dom";

function MyNavBar() {
  //color theme
  const currentTheme = useSelector((state) => state.currentTheme);
  const dispatch = useDispatch();
  return (
    <div fixed="top">
      <Navbar
        collapseOnSelect
        expand="lg"
        bg={currentTheme.variant}
        variant="dark"
      >
        <Container>
          <Navbar.Brand href="home">Welcome to Trendr</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="ms-auto">
              <Nav.Link as={Link} to="/home">
                Home
              </Nav.Link>
              <Nav.Link as={Link} to="/account">
                MyAccount
              </Nav.Link>
              <Nav.Link as={Link} to="/report">
                MyReport
              </Nav.Link>
              <Nav.Link as={Link} to="/about" style={{ marginRight: "20px" }}>
                About
              </Nav.Link>
              <Button
                variant={currentTheme.variant}
                onClick={() => dispatch(toggleTheme())}
              >
                {currentTheme.name} Mode
              </Button>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <br />
    </div>
  );
}

export default MyNavBar;
