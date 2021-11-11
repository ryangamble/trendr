import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Navbar, Container, Nav, Button } from 'react-bootstrap'
import { Link, useHistory } from 'react-router-dom'

import axios from 'axios'
import { removeUser } from '../Theme/userActions'

function MyNavBar () {
  // color theme
  const currentTheme = useSelector((state) => state.theme.currentTheme)
  // current user
  const currentUser = useSelector((state) => state.user)
  const dispatch = useDispatch()
  const history = useHistory()

  const handleLoginClick = () => {
    // if user is not logged in, we redirect to login page
    if (currentUser.username === '' && currentUser.email === '') {
      // TODO: remove this logout once session recovery is implemented
      // make a logout request
      axios
        .post('http://localhost:5000/auth/logout', {}, { withCredentials: true })
        .then((res) => {
          // remove the global user
          dispatch(removeUser())

          history.push('/login')
        })
        .catch((error) => {
          alert(JSON.stringify(error.response.data.response.errors))

          // if we get an error here we are already logged out...

          // remove the global user
          dispatch(removeUser())

          history.push('/login')
        })

      // history.push("/login");
    } else {
      // make a logout request
      axios
        .post('http://localhost:5000/auth/logout', {}, { withCredentials: true })
        .then((res) => {
          // remove the global user
          dispatch(removeUser())

          alert('You have been logged out!')
          history.push('/home')
        })
        .catch((error) => {
          alert(JSON.stringify(error.response.data.response.errors))

          // if we get an error here we are already logged out...

          // remove the global user
          dispatch(removeUser())

          alert('You have been logged out!')
          history.push('/home')
        })
    }
  }
  return (
    <div fixed="top">
      <Navbar
        collapseOnSelect
        expand="lg"
        bg={currentTheme.variant}
        variant="dark"
      >
        <Container>
          <Navbar.Brand as={Link} to="/home" style={{ fontSize: '2em' }}>
            Trendr
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="ms-auto">
              <Nav.Link as={Link} to="/home">
                Home
              </Nav.Link>
              <Nav.Link as={Link} to="/myaccount">
                MyAccount
              </Nav.Link>
              <Nav.Link as={Link} to="/settings">
                Settings
              </Nav.Link>
              <Nav.Link as={Link} to="/report">
                MyReport
              </Nav.Link>
              <Nav.Link as={Link} to="/about">
                About
              </Nav.Link>
              <Button variant={currentTheme.variant} onClick={handleLoginClick}>
                {currentUser.username === '' && currentUser.email === ''
                  ? 'Login/Register'
                  : 'Log Out'}
              </Button>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <br />
    </div>
  )
}

export default MyNavBar
