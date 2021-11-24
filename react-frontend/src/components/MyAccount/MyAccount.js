import React, { useState, useEffect } from 'react'
import MyNavBar from '../NavBar/MyNavBar'
import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import {
  Col,
  Container,
  ListGroup,
  Row,
  Badge,
  Button,
  ListGroupItem,
  Card,
  Form
} from 'react-bootstrap'
import './MyAccount.css'
import FollowBtn from '../FollowButton/FollowBtn'
import axios from 'axios'

function MyAccount () {
  // color theme
  const currentTheme = useSelector((state) => state.theme.currentTheme)
  // current user
  const currentUser = useSelector((state) => state.user)

  // List of followed stocks/cryptos
  const [list, setList] = useState([])

  const [oldPassword, setOldPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  useEffect(() => {
    // get the user follow list
    if (currentUser.email !== '' || currentUser.username !== '') {
      console.log('profile fetching user follow list....')

      axios
        .get(`/api/users/assets-followed`, {
          withCredentials: true
        })
        .then((res) => {
          return res.data
        })
        .then((data) => {
          console.log(data)
          console.log(data.assets)
          setList(data.assets)
        })
        .catch((error) => {
          alert(JSON.stringify(error.response.data.response.errors))
        })
    }
  }, [])

  const unfollowCallback = (item) => {
    setList(list.filter((x) => x !== item))
  }

  const handleChangePassword = (e) => {
    e.preventDefault()
    // check if 2 passwords are the same
    if (confirmPassword !== newPassword) {
      alert('Your new passwords are not the same!')
      return
    }

    const json = JSON.stringify({
      password: oldPassword,
      new_password: newPassword,
      new_password_confirm: confirmPassword
    })
    const config = {
      headers: { 'Content-Type': 'application/json' },
      withCredentials: true
    }
    console.log('changing password')
    axios
      .post(`/api/auth/change`, json, config)
      .then((res) => {
        alert('Your password has been changed successfully!')
        // Clear the input
        setOldPassword('')
        setNewPassword('')
        setConfirmPassword('')
      })
      .catch(() => {
        alert(
          'Change password failed, make sure your old password is correct and your new password is complex!'
        )
      })
  }

  return (
    <div
      style={{
        backgroundColor: currentTheme.background,
        height: '100vh',
        color: currentTheme.foreground
      }}
      className="myAccountWrapper"
    >
      <MyNavBar />

      <Container>
        <Row align="left">
          <Col xs={12} md={3}>
            <h3>
              Welcome{' '}
              {currentUser.username === '' && currentUser.email === ''
                ? 'Guest!'
                : currentUser.email}
            </h3>

            {currentUser.username === '' && currentUser.email === ''
              ? (
              <Link to="login">Login to see your profile</Link>
                )
              : null}
          </Col>
        </Row>

        <br />
        <br />
        {currentUser.username === '' && currentUser.email === ''
          ? null
          : (
          <div>
            <Row>
              <Col xs={12} md={3}>
                <h3>
                  <Badge bg="info">Your Followed Cryptos/Stocks:</Badge>
                </h3>
              </Col>
            </Row>
            {list.length === 0
              ? (
              <p>You haven&apos;t followed any stocks/cryptos.</p>
                )
              : null}
            <Row>
              <Col xs={12}>
                <ListGroup variant="flush" align="left">
                  {list.map((item) => (
                    <ListGroupItem
                      variant={currentTheme.name.toLowerCase()}
                      action
                      key={item}
                    >
                      <Link
                        to={{
                          pathname: `/result/${item}`
                        }}
                      >
                        {item.split(':')[1].toUpperCase()}
                      </Link>
                      <FollowBtn
                        id={item}
                        isFollow={true}
                        callback={unfollowCallback}
                      />
                    </ListGroupItem>
                  ))}
                </ListGroup>
              </Col>
            </Row>
          </div>
            )}
        <br />
        {currentUser.username === '' && currentUser.email === ''
          ? null
          : (
          <Row>
            <Col sm="12" md="6" lg="3">
              <Card>
                <Card.Header
                  style={{ color: currentTheme.textColorLightBackground }}
                >
                  Change Your Password Here
                </Card.Header>
                <Card.Body>
                  <Form onSubmit={handleChangePassword}>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                      <Form.Control
                        type="password"
                        placeholder="Enter your old password"
                        required
                        value={oldPassword}
                        onChange={(e) => setOldPassword(e.target.value)}
                        style={{ marginBottom: '5px' }}
                      />

                      <Form.Control
                        type="password"
                        placeholder="Enter your new password"
                        required
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        style={{ marginBottom: '5px' }}
                      />
                      <Form.Control
                        type="password"
                        placeholder="Confirm your new password"
                        required
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                      />
                    </Form.Group>

                    <Row>
                      <Col>
                        <Button variant={currentTheme.variant} type="submit">
                          Change Password
                        </Button>
                      </Col>
                    </Row>
                  </Form>
                </Card.Body>
              </Card>
            </Col>
          </Row>
            )}
      </Container>
    </div>
  )
}

export default MyAccount
