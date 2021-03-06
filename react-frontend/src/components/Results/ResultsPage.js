import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useParams, Link } from 'react-router-dom'
import MyNavBar from '../NavBar/MyNavBar'
import TweetSummary from './TweetSummary'
import { Container, Col, Row } from 'react-bootstrap'
import {
  SentimentGraph,
  PriceVolumeGraph,
  TopTokenHolders,
  MentionsGraph
} from './Graph'
import { StockStatistics, CoinStatistics, TokenStatistics } from './Statistics'
import FollowBtn from '../FollowButton/FollowBtn'
import axios from 'axios'

function Results (props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme)
  // const currentCurrency = useSelector((state) => state.currency.currentCurrency)
  // current user
  const currentUser = useSelector((state) => state.user)

  const { id } = useParams()
  const [isFollow, setIsFollow] = useState(false)
  const [type, setType] = useState(null)
  const [symbol, setSymbol] = useState(null)
  const [addr, setAddr] = useState(null)

  useEffect(() => {
    console.log('id is', id)
    console.log(id.substring(0, id.indexOf(':')))
    setType(id.substring(0, id.indexOf(':')))
    if (id.lastIndexOf(':') !== id.indexOf(':')) {
      setAddr(id.substring(id.lastIndexOf(':') + 1))
      setSymbol(id.substring(id.indexOf(':') + 1, id.lastIndexOf(':')))
    } else {
      setSymbol(id.substring(id.indexOf(':') + 1))
      console.log(id.substring(id.indexOf(':') + 1))
    }
  }, [id])

  useEffect(() => {
    // do this only if user is logged in
    if ((currentUser.email !== '' || currentUser.username !== '') && type && symbol) {
      axios
        .post('http://localhost:5000/users/result-history', {
          symbol: symbol,
          type: type
        }, { withCredentials: true })
        .catch(() => {
          alert('Could not update result history')
        })
    }
  }, [type, symbol])

  useEffect(() => {
    // do this only if user is logged in
    if (currentUser.email !== '' || currentUser.username !== '') {
      console.log('fetching user follow list')

      axios
        .get('http://localhost:5000/users/assets-followed', {
          withCredentials: true
        })
        .then((res) => {
          return res.data
        })
        .then((data) => {
          console.log(data)
          console.log(data.assets, id)
          if (data.assets.includes(id)) {
            setIsFollow(true)
            console.log('yes', props.location, props.location.state)
          }
        })
        .catch((error) => {
          alert(JSON.stringify(error.response.data.response.errors))
        })
    }
  }, [])

  return (
    <>
    {(symbol === null || type === null)
      ? (
          null
        )
      : (
      <div
        className="resultsPage"
        style={{
          background: currentTheme.background,
          color: currentTheme.foreground
        }}
      >
        <MyNavBar />
        <br />
        <br />
        <Container className="resultsContainer">
          <Row>
            <Col xs={12} className="resultsHeader">
              <h3 style={{ marginRight: 10 }}>
                Showing Results For: {symbol.toUpperCase()}
              </h3>
              {currentUser.username === '' &&
              currentUser.email === ''
                ? null
                : (
                <FollowBtn id={id} isFollow={isFollow} />
                  )}
            </Col>
          </Row>
          <br />
          <Row>
            <Col xs={12} sm={12} md={12} lg={6}>
              {type === 'crypto' ? <CoinStatistics id={symbol} /> : <StockStatistics symbol={symbol} />}
              <br />
              <SentimentGraph symbol={symbol} type={type}/>
              <br />
              <TweetSummary symbol={symbol}/>
              <br />
              {addr && (
                <>
                  <TopTokenHolders addr={addr} />
                  <br />
                </>
              )}
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              <PriceVolumeGraph symbol={symbol} assetType={type} graphType="price" color="#228B22" />
              <br />
              <PriceVolumeGraph symbol={symbol} assetType={type} graphType="volume" color="orange" />
              <br />
              <MentionsGraph symbol={symbol} />
              <br />
              {addr && (
                <>
                  <TokenStatistics addr={addr} />
                  <br />
                </>
              )}
            </Col>
          </Row>
          <Link to="../../home" style={{ color: currentTheme.linkColor }}>
            Return to Home
          </Link>
        </Container>

      </div>
        )}
    </>
  )
}

export default Results
