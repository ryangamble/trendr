import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useParams, Link } from 'react-router-dom'
import MyNavBar from '../NavBar/MyNavBar'
import TweetSummary from './TweetSummary'
import { Container, Col, Row, Spinner } from 'react-bootstrap'
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
  // current user
  const currentUser = useSelector((state) => state.user)

  const { id } = useParams()
  const [currency, setCurrency] = useState(null)
  const [isFollow, setIsFollow] = useState(false)
  const [type, setType] = useState(null)
  const [symbol, setSymbol] = useState(null)
  const [addr, setAddr] = useState(null)

  const setCurrencyCallback = (curr) => {
    setCurrency(curr)
  }

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
        .get(`${process.env.REACT_APP_API_ROOT}/users/assets-followed`, {
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

  if (type && symbol) {
    if (type === 'crypto') {
      return renderCryptoResults()
    } else {
      return renderStockResults()
    }
  } else {
    return null
  }

  function renderStockResults () {
    return (
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
              <h3 style={{ marginRight: 10 }}>Showing Results For: {symbol}</h3>
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
              <StockStatistics
                symbol={symbol}
                currencyCallback={setCurrencyCallback}
              />
              <br />
              <SentimentGraph symbol={symbol} />
              <br />
              <TweetSummary symbol={symbol}/>
              <br />
            </Col>
            <Col xs={12} sm={12} md={12} lg={6}>
              {currency
                ? (
                <PriceVolumeGraph
                  symbol={symbol}
                  currency={currency}
                  assetType="stock"
                  graphType="price"
                  color="#0D6EFD"
                />
                  )
                : (
                <Container fluid>
                  <Spinner animation="border" />
                </Container>
                  )}
              <br />
              {currency
                ? (
                <PriceVolumeGraph symbol={symbol} assetType="stock" graphType="volume" color="orange" />
                  )
                : (
                <Container fluid>
                  <Spinner animation="border" />
                </Container>
                  )}
              <br />
              <MentionsGraph symbol={symbol} />
              <br />
            </Col>
          </Row>
          <Link to="../../home" style={{ color: currentTheme.linkColor }}>
            Return to Home
          </Link>
        </Container>
      </div>
    )
  }

  function renderCryptoResults () {
    return (
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
              <CoinStatistics id={symbol} />
              <br />
              <SentimentGraph symbol={symbol} />
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
              <PriceVolumeGraph symbol={symbol} currency="usd" assetType="crypto" graphType="price" color="#228B22" />
              <br />
              <PriceVolumeGraph symbol={symbol} assetType="crypto" graphType="volume" color="orange" />
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
    )
  }
}

export default Results
