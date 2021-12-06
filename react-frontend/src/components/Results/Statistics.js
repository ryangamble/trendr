import React, { useEffect, useState } from 'react'
import {
  Container,
  Image,
  Table,
  Col,
  Spinner,
  OverlayTrigger,
  Tooltip
} from 'react-bootstrap'
import { useSelector } from 'react-redux'
import axios from 'axios'
import './Results.css'

const getNumberUnit = (num) => {
  if (num < 1000000) {
    return num
  }
  const units = ['M', 'B', 'T']
  const unit = Math.floor((num / 1.0e1).toFixed(0).toString().length)
  const r = unit % 3
  const x = Math.abs(Number(num)) / Number('1.0e+' + (unit - r)).toFixed(2)
  if (units[Math.floor(unit / 3) - 2] === undefined) {
    return Number.parseInt(num).toExponential(4)
  }
  return x.toFixed(2) + ' ' + units[Math.floor(unit / 3) - 2]
}

function StockStatistics (props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme)

  const [asset, setAsset] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    axios
      .get('http://localhost:5000/assets/stock/stats', {
        method: 'GET',
        params: {
          symbol: props.symbol
        }
      })
      .then((res) => {
        const data = res.data
        setAsset({
          companyName: data.longName ? data.longName : data.shortName,
          logo: data.logo_url,
          symbol: data.symbol,
          currency: data.currency ? data.currency : 'USD',
          dayOpen: data.open,
          dayHigh: data.dayHigh,
          dayLow: data.dayLow,
          fiftyTwoWeekHigh: data.fiftyTwoWeekHigh,
          fiftyTwoWeekLow: data.fiftyTwoWeekLow,
          volume: data.volume.toLocaleString('en-US'),
          avgVolume: data.averageVolume.toLocaleString('en-US'),
          marketCap: data.marketCap
            ? getNumberUnit(data.marketCap)
            : 'N/A',
          pegRatio: data.pegRatio ? data.pegRatio.toFixed(2) : 'N/A',
          divYield: data.dividendYield
            ? (data.dividendYield * 100).toFixed(2)
            : 'N/A',
          website: data.website
        })
        props.currencyCallback(data.currency)

        axios
          .get('http://localhost:5000/assets/stocks/listed-exchanges', {
            method: 'GET',
            params: {
              symbol: props.symbol
            }
          })
          .then((res) => {
            console.log(res.data)
            setAsset(prevData => { return { ...prevData, exchanges: res.data } })
          })
          .catch((error) => {
            console.log(error)
            setAsset(prevData => { return { ...prevData, exchanges: false } })
          })
      })
      .then(() => {
        setLoading(false)
      })
      .catch((error) => {
        console.log(error)
      })
  }, [props.symbol])

  function formatPrice (num) {
    if (num < 0.1) {
      return num.toFixed(7)
    }
    const options = {
      style: 'currency',
      currency: 'usd'
    }
    return num.toLocaleString('en-US', options)
  }

  function renderExchanges () {
    if (!asset.exchanges) {
      return (null)
    }
    const list = []
    for (const key in asset.exchanges) {
      list.push(<div key={key}>{asset.exchanges[key]}<br/></div>)
    }
    return (list)
  }

  return (
    <>
      {loading
        ? (
        <Container fluid>
          <Spinner animation="border" />
        </Container>
          )
        : (
        <Container fluid>
          <Col>
            <Image src={asset.logo} rounded alt="<no logo>"/>
            <h2>{asset.companyName}</h2>
            <p>{asset.symbol}</p>
            { asset.website && <a href={asset.website} target="_blank" rel="noreferrer">Homepage</a>}
          </Col>
          <Col>
            <Table size="sm" style={{ color: currentTheme.foreground }}>
              <tbody>
                <tr>
                  <td className="statName">Currency</td>
                  <td className="statValue">{asset.currency}</td>
                </tr>
                <tr>
                  <td className="statName">Day Open</td>
                  <td className="statValue">{formatPrice(asset.dayOpen)}</td>
                </tr>
                <tr>
                  <td className="statName">Day High</td>
                  <td className="statValue">{formatPrice(asset.dayHigh)}</td>
                </tr>
                <tr>
                  <td className="statName">Day Low</td>
                  <td className="statValue">{formatPrice(asset.dayLow)}</td>
                </tr>
                <tr>
                  <td className="statName">52 Week High</td>
                  <td className="statValue">
                    {formatPrice(asset.fiftyTwoWeekHigh)}
                  </td>
                </tr>
                <tr>
                  <td className="statName">52 Week Low</td>
                  <td className="statValue">
                    {formatPrice(asset.fiftyTwoWeekLow)}
                  </td>
                </tr>
                <tr>
                  <td className="statName">Volume</td>
                  <td className="statValue">{asset.volume}</td>
                </tr>
                <tr>
                  <td className="statName">Avg. Volume</td>
                  <td className="statValue">{asset.avgVolume}</td>
                </tr>
                <tr>
                  <td className="statName">Div/Yield</td>
                  <td className="statValue">{asset.divYield}</td>
                </tr>
                <tr>
                  <td className="statName">PEG ratio</td>
                  <td className="statValue">{asset.pegRatio}</td>
                </tr>
                <tr>
                  <td className="statName">Market Cap</td>
                  <td className="statValue">
                    {formatPrice(Number(asset.marketCap.slice(0, -1))) +
                      asset.marketCap.slice(-1)}
                  </td>
                </tr>
                <tr>
                  <td className="statName">Exchanges</td>
                  <td className="statValue">{asset.exchanges != null ? renderExchanges() : <Spinner animation="border" size="sm"/>}</td>
                </tr>
              </tbody>
            </Table>
          </Col>
        </Container>
          )}
    </>
  )
}

function CoinStatistics (props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme)

  const [crypto, setCrypto] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    axios
      .get('http://localhost:5000/assets/crypto/stats', {
        method: 'GET',
        params: {
          id: props.id
        }
      })
      .then((res) => {
        const data = res.data
        console.log(data)
        setCrypto(data)
      })
      .then(() => {
        setLoading(false)
      })
      .catch((error) => {
        console.log(error)
      })
  }, [props.id])

  function formatPrice (num) {
    if (num == null) return 'Not available'
    if (num < 0.1) {
      return '$' + num.toFixed(7).toString()
    }
    const options = {
      style: 'currency',
      currency: 'usd'
    }
    return num.toLocaleString('en-US', options)
  }

  function renderExchanges () {
    if (crypto.exchanges.length === 0) {
      return ('Not available')
    } else if (crypto.exchanges.length > 5) {
      return (
        <div>
          {crypto.exchanges[0]}
          <OverlayTrigger
            placement="auto"
            overlay={renderTooltip()}
          >
            <div>...</div>
          </OverlayTrigger>
        </div>
      )
    }
    const list = []
    for (const key in crypto.exchanges) {
      list.push(<div key={key}>{crypto.exchanges[key]}<br/></div>)
    }
    return (list)
  }

  function renderTooltip () {
    const list = []
    for (const key in crypto.exchanges) {
      list.push(crypto.exchanges[key] + ', ')
    }
    list[list.length - 1] = list[list.length - 1].substring(0, list[list.length - 1].lastIndexOf(','))
    return (
      <Tooltip>
        {list}
      </Tooltip>
    )
  }

  return (
    <>
      {loading
        ? (
        <Container fluid>
          <Spinner animation="border" />
        </Container>
          )
        : (
        <Container fluid>
          <Col>
          <Col>
            <Image src={crypto.Image} rounded />
            <h2>{crypto.Name}</h2>
            <p>{crypto.Symbol.toUpperCase()}</p>
            {crypto.homepage && <a href={crypto.homepage} target="_blank" rel="noreferrer">Homepage</a>}
          </Col>
          </Col>
          <Col>
            <Table size="sm" style={{ color: currentTheme.foreground }}>
              <tbody>
                <tr>
                  <td className="statName">Price</td>
                  <td className="statValue">{formatPrice(crypto.Price)}</td>
                </tr>
                <tr>
                  <td className="statName">Day High</td>
                  <td className="statValue">{formatPrice(crypto.DayHigh)}</td>
                </tr>
                <tr>
                  <td className="statName">Day Low</td>
                  <td className="statValue">{formatPrice(crypto.DayLow)}</td>
                </tr>
                <tr>
                  <td className="statName">Market Cap Rank</td>
                  <td className="statValue">{crypto.MarketCapRank ? crypto.MarketCapRank : 'Not available'}</td>
                </tr>
                <tr>
                  <td className="statName">24 Hour Market Cap Change</td>
                  <td className="statValue">{crypto['24HrMarketCapChange'] ? crypto['24HrMarketCapChange'] + '%' : 'Not available'}</td>
                </tr>
                <tr>
                  <td className="statName">24 Hour Price Change</td>
                  <td className="statValue">{crypto['24HrPriceChange'] ? crypto['24HrPriceChange'] + '%' : 'Not available'}</td>
                </tr>
                <tr>
                  <td className="statName">Market Cap</td>
                  <td className="statValue">{formatPrice(crypto.MarketCap)}</td>
                </tr>
                <tr>
                  <td className="statName">Exchanges</td>
                  <td className="statValue">{crypto.exchanges && renderExchanges()}</td>
                </tr>
              </tbody>
            </Table>
          </Col>
        </Container>
          )}
    </>
  )
}

function TokenStatistics (props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme)

  const [token, setToken] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // console.log(props.addr)
    setLoading(true)
    axios
      .get('http://localhost:5000/assets/token/info', {
        method: 'GET',
        params: {
          address: props.addr
        }
      })
      .then((res) => {
        setLoading(true)
        return JSON.parse(JSON.stringify(res.data))
      })
      .then((data) => {
        console.log(data)
        setToken(data)
      })
      .then(() => {
        setLoading(false)
      })
      .catch((error) => {
        console.log(error)
      })
  }, [props.addr])

  return (
    <>
      {loading
        ? (
        <Container fluid>
          <Spinner animation="border" />
        </Container>
          )
        : (
        <Container fluid>
          <Col>
            <h2 style={{ textAlign: 'left' }}>Token Info</h2>
            <Table size="sm" style={{ color: currentTheme.foreground }}>
              <tbody>
                <tr>
                  <td className="statName">Address</td>
                  <td className="statValue">{token.address}</td>
                </tr>
                <tr>
                  <td className="statName">Total Holders</td>
                  <td className="statValue">{token.holdersCount}</td>
                </tr>
                <tr>
                  <td className="statName">Total Supply</td>
                  <td className="statValue">{getNumberUnit(token.totalSupply)}</td>
                </tr>
                <tr>
                  <td className="statName">Price</td>
                  <td className="statValue">{token.price.rate}</td>
                </tr>
                <tr>
                  <td className="statName">Total Operations</td>
                  <td className="statValue">{token.countOps}</td>
                </tr>
              </tbody>
            </Table>
          </Col>
        </Container>
          )}
    </>
  )
}

export {
  StockStatistics,
  CoinStatistics,
  TokenStatistics
}
