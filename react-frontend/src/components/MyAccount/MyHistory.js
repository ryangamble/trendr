import React, { useState, useEffect } from 'react'
import MyNavBar from '../NavBar/MyNavBar'
import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import {
  Col,
  Container,
  ListGroup,
  Row,
  ListGroupItem
} from 'react-bootstrap'
import './MyAccount.css'
import axios from 'axios'

function MyHistory () {
  // color theme
  const currentTheme = useSelector((state) => state.theme.currentTheme)
  // current user
  const currentUser = useSelector((state) => state.user)

  // List of followed stocks/cryptos
  const [list, setList] = useState([])

  useEffect(() => {
    // get the user follow list
    if (currentUser.email !== '' || currentUser.username !== '') {
      console.log('profile fetching user follow list....')

      axios
        .get('http://localhost:5000/users/result-history', {
          withCredentials: true
        })
        .then((res) => {
          return res.data
        })
        .then((data) => {
          console.log(`DATA: ${data}`)
          setList(data)
        })
        .catch(() => {
          alert('Could not retrieve search history.')
        })
    }
  }, [])

  return (
    <div
      style={{
        backgroundColor: currentTheme.background,
        height: '100vh',
        color: currentTheme.foreground
      }}
      className="myHistoryWrapper"
    >
      <MyNavBar />

      <Container>
        <Row align="left">
          <Col xs={12} md={3}>
            <h3>Search History</h3>

            {currentUser.username === '' && currentUser.email === ''
              ? (
              <Link to="login">Login to see your search history</Link>
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
            {list.length === 0
              ? (
              <p>You haven&apos;t made any searches.</p>
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
                      <p>Asset: </p>
                      <Link
                        to={{
                          pathname: `/result/${item.type}:${item.symbol}`
                        }}
                      >
                        {item.symbol.toUpperCase()}
                      </Link>
                      <p> ({item.type})</p>
                      <p className="floatRight">Searched at: {item.ran_at}</p>
                    </ListGroupItem>
                  ))}
                </ListGroup>
              </Col>
            </Row>
          </div>
            )}
        <br />
      </Container>
    </div>
  )
}

export default MyHistory
