import React, { useEffect, useState } from 'react'
import {
  Container,
  Spinner,
  Row,
  Col,
  ButtonGroup,
  Button,
  Table
} from 'react-bootstrap'

import { useSelector } from 'react-redux'

import {
  XAxis,
  YAxis,
  HorizontalGridLines,
  VerticalGridLines,
  FlexibleXYPlot,
  RadialChart,
  LineSeries,
  LineMarkSeries,
  MarkSeries,
  Voronoi,
  Crosshair,
  Borders,
  DiscreteColorLegend,
  makeVisFlexible
} from 'react-vis'

import axios from 'axios'
import './Results.css'
import ImportantPosts from './ImportantPosts'
import '../../../node_modules/react-vis/dist/style.css'

const FlexRadialChart = makeVisFlexible(RadialChart)

// Currently pass symbol as a prop, can be changed later
// Used for both price and volume charts for stocks and cryptos
function PriceVolumeGraph (props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme)
  const currentCurrency = useSelector((state) => state.currency.currentCurrency)

  const [graphData, setGraphData] = useState([])

  const [min, setMin] = useState(0)
  const [max, setMax] = useState(0)
  const [loadedCount, setLoadedCount] = useState(0)
  const [crosshairValues, setCrosshairValues] = useState([])
  const [period, setPeriod] = props.assetType === 'crypto' ? useState('1') : useState('1d')

  const periodDisplay = props.assetType === 'crypto'
    ? {
        1: 'Past Day',
        5: 'Past 5 Days',
        30: 'Past Month',
        90: 'Past 3 Months',
        365: 'Past Year'
      }
    : {
        '1d': 'Past Day',
        '5d': 'Past 5 Days',
        '1mo': 'Past Month',
        '3mo': 'Past 3 Months',
        '1y': 'Past Year'
      }

  useEffect(() => {
    setLoadedCount(0)
    for (const key in periodDisplay) {
      console.log('fetching ' + props.graphType + ' data for ' + key + '...')
      props.assetType === 'crypto' ? fetchCryptoDataPoints(key) : fetchStockDataPoints(key)
    }
  }, [])

  useEffect(() => {
    console.log(props.currency)
    getMinMax()
    console.log('changing ' + props.graphType + ' period to ' + period)
  }, [period, loadedCount])

  async function fetchStockDataPoints (timePeriod) {
    axios
      .get(`${process.env.REACT_APP_API_ROOT}/assets/stock/history`, {
        method: 'GET',
        params: {
          symbol: props.symbol,
          currency: currentCurrency,
          period: timePeriod
        }
      })
      .then((res) => {
        return JSON.parse(JSON.stringify(res.data))
      })
      .then((data) => {
        const pd = []
        let tableCol = ''
        if (props.graphType === 'price') {
          tableCol = 'Close'
        } else {
          tableCol = 'Volume'
        }
        // console.log(data[tableCol])
        for (const key in data[tableCol]) {
          // console.log(key)
          // console.log(data['Close'][key].toFixed(2))
          const value = data[tableCol][parseInt(key)]
          if (typeof (value) !== 'number') {
            continue
          }

          if (props.graphType === 'price') {
            pd.push({
              x: unixToUTC(key),
              y: value.toFixed(2)
            })
          } else if (value > 0) {
            pd.push({
              x: unixToUTC(key),
              y: value
            })
          }
        }
        return pd
      })
      .then((pd) => {
        console.log(pd)
        const min = Number.MAX_VALUE
        const max = 0
        switch (timePeriod) {
          case '1d':
            setGraphData((prev) => ({ ...prev, '1d': pd }))
            break
          case '5d':
            setGraphData((prev) => ({ ...prev, '5d': pd }))
            break
          case '1mo':
            setGraphData((prev) => ({ ...prev, '1mo': pd }))
            break
          case '3mo':
            setGraphData((prev) => ({ ...prev, '3mo': pd }))
            break
          case '1y':
            setGraphData((prev) => ({ ...prev, '1y': pd }))
            break
          default:
            setGraphData((prev) => ({ ...prev, '1d': pd }))
        }
        return [min, max]
      })
      .then(() => {
        console.log(props.graphType + ' data loaded for ' + timePeriod)
        setLoadedCount((prevCount) => prevCount + 1)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  async function fetchCryptoDataPoints (timePeriod) {
    let apiRoute = ''
    if (props.graphType === 'price') {
      apiRoute = `${process.env.REACT_APP_API_ROOT}/assets/crypto/price-history`
    } else {
      apiRoute = `${process.env.REACT_APP_API_ROOT}/assets/crypto/volume-history`
    }

    axios
      .get(apiRoute, {
        method: 'GET',
        params: {
          id: props.symbol,
          currency: currentCurrency,
          days: timePeriod
        }
      })
      .then((res) => {
        return JSON.parse(JSON.stringify(res.data))
      })
      .then((data) => {
        const pd = []
        for (let i = 0; i < data.length; i++) {
          pd.push({
            x: data[i.toString()]['0'],
            y: parseFloat(data[i.toString()]['1'])
          })
        }
        return pd
      })
      .then((pd) => {
        console.log(pd)
        const min = Number.MAX_VALUE
        const max = 0
        switch (timePeriod) {
          case '1':
            setGraphData((prev) => ({ ...prev, 1: pd }))
            break
          case '5':
            setGraphData((prev) => ({ ...prev, 5: pd }))
            break
          case '30':
            setGraphData((prev) => ({ ...prev, 30: pd }))
            break
          case '90':
            setGraphData((prev) => ({ ...prev, 90: pd }))
            break
          case '365':
            setGraphData((prev) => ({ ...prev, 365: pd }))
            break
          default:
            setGraphData((prev) => ({ ...prev, 1: pd }))
        }
        return [min, max]
      })
      .then(() => {
        console.log(props.graphType + ' data loaded for ' + timePeriod + ' days')
        setLoadedCount((prevCount) => prevCount + 1)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  function getMinMax () {
    let min = Number.MAX_VALUE
    let max = 0
    for (const key in graphData[period]) {
      const val = graphData[period][key].y
      if (val > max) {
        max = val
      }
      if (val < min) {
        min = val
      }
    }
    setMin(min)
    setMax(max)
    // console.log(min);
  }

  const _onMouseLeave = () => {
    setCrosshairValues([])
  }

  const _onNearestX = (value) => {
    const x = value.x.toString()
    value.x = x
    setCrosshairValues([value])
  }

  const itemsFormatPrice = (data) => {
    return [{ title: 'price', value: formatPrice(data[0].y) }]
  }

  const itemsFormatVol = (data) => {
    return [{ title: 'volume', value: data[0].y.toLocaleString('en-US') }]
  }

  const unixToUTC = (unix) => {
    let date = new Date(parseInt(unix)).toString()
    date = date.replace(' ', ', ')
    return date.substring(0, date.indexOf('-'))
  }

  const formatPrice = (num) => {
    if (Math.abs(num) < 0.1) {
      return num.toFixed(7)
    }
    const options = {
      style: 'currency',
      currency: currentCurrency.toLowerCase()
    }
    return num.toLocaleString('en-US', options)
  }

  const renderButtons = () => {
    return (
      <ButtonGroup size="sm">
        <Button
          variant="secondary"
          className={props.graphType + 'PeriodToggle'}
          onClick={() => {
            props.assetType === 'crypto' ? setPeriod('1') : setPeriod('1d')
          }}
        >
          1D
        </Button>
        <Button
          variant="secondary"
          className={props.graphType + 'PeriodToggle'}
          onClick={() => {
            props.assetType === 'crypto' ? setPeriod('5') : setPeriod('5d')
          }}
        >
          5D
        </Button>
        <Button
          variant="secondary"
          className={props.graphType + 'PeriodToggle'}
          onClick={() => {
            props.assetType === 'crypto' ? setPeriod('30') : setPeriod('1mo')
          }}
        >
          1M
        </Button>
        <Button
          variant="secondary"
          className={props.graphType + 'PeriodToggle'}
          onClick={() => {
            props.assetType === 'crypto' ? setPeriod('90') : setPeriod('3mo')
          }}
        >
          3M
        </Button>
        <Button
          variant="secondary"
          className={props.graphType + 'PeriodToggle'}
          onClick={() => {
            props.assetType === 'crypto' ? setPeriod('365') : setPeriod('1y')
          }}
        >
          1Y
        </Button>
      </ButtonGroup>
    )
  }

  return (
    <>
      { loadedCount < 5
        ? (
        <Container fluid>
          <Spinner animation="border" />
        </Container>
          )
        : (
        <Container className="graphLayout">
          <Row>
            <div className="chartTitle">
              {props.graphType === 'price'
                ? (
                <h2>Price history</h2>
                  )
                : (
                <h2>Volume history</h2>
                  )}
            </div>
          </Row>
          <Row>
            <div className="chartContainer">
              <FlexibleXYPlot
                onMouseLeave={_onMouseLeave}
                xType="ordinal"
                yDomain={
                  props.graphType === 'price'
                    ? [0.98 * min, 1.02 * max]
                    : [0.9 * min, 1.2 * max]
                }
              >
                <HorizontalGridLines />
                {/* <VerticalGridLines/> */}

                <LineSeries
                  animation={true}
                  data={graphData[period]}
                  onNearestX={_onNearestX}
                  strokeWidth={2}
                  opacity={1}
                  color={props.graphType === 'price'
                    ? (graphData[period][graphData[period].length - 1].y -
                    graphData[period][0].y > 0
                        ? ('#14ad14'
                          )
                        : (
                            '#dc4b4b')
                      )
                    : 'orange'}
                />
                <Borders
                  style={{
                    bottom: { fill: currentTheme.fill },
                    left: { fill: currentTheme.fill },
                    right: { fill: currentTheme.fill },
                    top: { fill: currentTheme.fill }
                  }}
                />

                <YAxis
                  title={props.graphType === 'price' ? 'Price' : 'Volume'}
                  style={{ title: { fill: currentTheme.foreground } }}
                />
                <XAxis
                  hideTicks
                  title="Time"
                />

                <Crosshair
                  values={crosshairValues}
                  titleFormat={(d) => {
                    return { title: 'Date', value: d[0].x }
                  }}
                  itemsFormat={
                    props.graphType === 'price'
                      ? itemsFormatPrice
                      : itemsFormatVol
                  }
                />
              </FlexibleXYPlot>
            </div>
          </Row>
          <Row>
            <Col>
              {renderButtons()}
            </Col>
            {props.graphType === 'price'
              ? (
              <Col>
                {graphData[period][graphData[period].length - 1].y -
                  graphData[period][0].y > 0
                  ? (
                  <div className="priceUp">
                    Up{' '}
                    {formatPrice(
                      graphData[period][graphData[period].length - 1].y -
                        graphData[period][0].y
                    )}{' '}
                    {periodDisplay[period]}
                  </div>
                    )
                  : (
                  <div className="priceDown">
                    Down{' '}
                    {formatPrice(
                      graphData[period][graphData[period].length - 1].y -
                        graphData[period][0].y
                    )}{' '}
                    {periodDisplay[period]}
                  </div>
                    )}
              </Col>
                )
              : (
              <Col></Col>
                )}
          </Row>
        </Container>
          )}
    </>
  )
}

function SentimentGraph (props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme)

  const [showModal, setShowModal] = useState(false)
  const [points, setPoints] = useState(null)
  const [hoveredNode, setHoveredNode] = useState(null)
  const [type, setType] = useState(null)
  const [posts, setPosts] = useState(null)

  // const [crosshairValues, setCrosshairValues] = useState(null)
  // const [selectedPointId, setSelectedPointId] = useState(null)

  useEffect(() => {
    // perform asset search once each time user searches
    assetSearch()
    fetchSentimentData(false)
  }, [])

  function assetSearch () {
    axios(`${process.env.REACT_APP_API_ROOT}/assets/perform_asset_search`, {
      method: 'GET',
      params: {
        symbol: props.type + ':' + props.symbol
      }
    }).then((res) => {
      console.log("Perfoming sentiment search for", props.symbol, res.data)
    }).catch((err) => {
      console.log(err);
    });
  }

  /*
    attempts to fetch the data, if its not there, backend calls perform_search_asset
  */

  function fetchSentimentData (searched) {
    const currentDate = Math.floor(Date.now() / 1000);
    const lastWeekDate = Math.floor((Date.now() - 604800000) / 1000);
    // call backend to fetch sentiment data
    axios(`${process.env.REACT_APP_API_ROOT}/assets/sentiment_values`, {
      method: 'GET',
      params: {
        asset_identifier: props.type + ':' + props.symbol,
        start_timestamp: lastWeekDate,
        end_timestamp: currentDate
      }
    })
      .then((res) => {
        const data = res.data.data;
        if (data == null || JSON.parse(JSON.stringify(data)).length === 0) {
          // continue to query sentiment_values endpoint on 30 sec interval until data is recieved
          setTimeout(() => {
            fetchSentimentData(true)
          }, 30000)
        }
        return data == null ? [] : JSON.parse(JSON.stringify(data))
      })
      .then((data) => {
        console.log(data)
        if (data.length === 0) {
          return null
        }
        const redditPoints = []
        const twitterPoints = []
        if (data.length > 1) {
          for (let i = 0; i < data.length; i++) {
            const redditSentiment = data[i.toString()].reddit_sentiment
            const twitterSentiment = data[i.toString()].twitter_sentiment

            if (redditSentiment != null && twitterSentiment != null) {
              redditPoints.push({
                x: unixToUTC(parseFloat(data[i.toString()].timestamp) * 1000),
                y: parseFloat(redditSentiment),
                type: 'Reddit'
              })

              twitterPoints.push({
                x: unixToUTC(parseFloat(data[i.toString()].timestamp) * 1000),
                y: parseFloat(twitterSentiment),
                type: 'Twitter'
              })
            }
          }
        }
        const p = [redditPoints, twitterPoints].map((p, i) => p.map(d => ({ ...d, line: i })))
        return p
      }).then((p) => {
        console.log(p)
        setPoints(p)
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const onClickHandler = (point) => {
    console.log('clickd on point', point)
    axios(`${process.env.REACT_APP_API_ROOT}/assets/sentiment_important_posts`, {
      method: 'GET',
      params: {
        asset_identifier: props.type + ':' + props.symbol,
        timestamp: (new Date(point.x).getTime() / 1000)
      }
    })
      .then((res) => {
        if (res.data == null) {
          return
        }
        setType(point.type)
        if (point.type === 'Twitter') {
          setPosts(res.data.data.tweets);
          console.log('important posts:', res.data.data.tweets)
        } else {
          setPosts(res.data.data.reddit_comments.concat(res.data.data.reddit_submissions))
          console.log('important posts:', res.data.data.reddit_comments, res.data.data.reddit_sentiment)
        }
      })
      .then(() => {
        setShowModal(true)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const unixToUTC = (unix) => {
    let date = new Date(parseInt(unix)).toString()
    date = date.replace(' ', ', ')
    return date.substring(0, date.indexOf('-'))
  }

  const timeAxisLabel = (date) => {
    const hour = date.substring(17, 19)
    if (hour === '00') {
      return date.substring(5, 11)
    }
    return ''
  }

  const formatSentimentPoint = (data) => {
    return [{ title: 'Sentiment Score', value: data[0].y }]
  }

  return (
    <>
    <ImportantPosts
      show={showModal}
      onHide={() => {
        setShowModal(false)
        setPosts(null)
      }}
      type={type}
      posts={posts}/>
    {points === null
      ? (
      <Container fluid>
        <Spinner animation="border" />
      </Container>
        )
      : (
          points[0].length === 0 && points[1].length === 0
            ? (
        <Container fluid>
          Sentiment data unavailable
        </Container>
              )
            : (
        <Container className="graphLayout">
          <Row>
            <div className="chartTitle">
              <h2>Sentiment Data</h2>
            </div>
          </Row>
          <Row>
            <div className="chartContainer">
              <FlexibleXYPlot
                xType="ordinal"
              >

                <HorizontalGridLines />
                <XAxis
                  title="Time"
                  tickFormat={xVal => `${timeAxisLabel(xVal)}`}
                  style={{ title: { fill: currentTheme.foreground } }}
                />
                <YAxis
                  title="Sentiment Score"
                  style={{ title: { fill: currentTheme.foreground } }}
                />
                <DiscreteColorLegend
                  orientation="horizontal"
                  style={{ position: 'absolute', right: '0%', top: '0%', backgroundColor: 'rgba(108,117,125, 0.7)', borderRadius: '5px' }}
                  items={[
                    {
                      title: 'Twitter',
                      color: '#0D6EFD',
                      strokeWidth: 5
                    },
                    {
                      title: 'Reddit',
                      color: 'red',
                      strokeWidth: 5
                    }
                  ]}
                />
                {points.map((d, i) => (
                  <LineMarkSeries
                    key={i}
                    opacity={0.5}
                    data={d}
                    color={i === 0 ? 'red' : '#0D6EFD'}
                  />
                ))}
                {hoveredNode && <MarkSeries
                  data={[hoveredNode]}
                  size={8}
                  />
                }
                {hoveredNode &&
                  <Crosshair
                    values={[hoveredNode]}
                    titleFormat={(d) => {
                      return { title: 'Date', value: d[0].x }
                    }}
                    itemsFormat={formatSentimentPoint}
                  />
                }
                <Voronoi
                  nodes={points.reduce((acc, d) => [...acc, ...d], [])}
                  onHover={node => setHoveredNode(node)}
                  onBlur={() => setHoveredNode(null)}
                  onClick={() => onClickHandler(hoveredNode)}
                  polygonStyle={{ stroke: null }}
                />
              </FlexibleXYPlot>
            </div>
          </Row>
        </Container>
              )
        )
      }
    </>
  )
}

function TopTokenHolders (props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme)

  const [graphData, setGraphData] = useState([])
  const [value, setValue] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)

    axios
      .get(`${process.env.REACT_APP_API_ROOT}/assets/token/top-holders`, {
        method: 'GET',
        params: {
          address: props.addr
        }
      })
      .then((res) => {
        return JSON.parse(JSON.stringify(res.data))
      })
      .then((data) => {
        const pd = []
        let totalShare = 0
        for (let i = 0; i < data.length; i++) {
          pd.push({
            theta: data[i.toString()].share * 3.6 / 1.8 * Math.PI,
            label: data[i.toString()].address,
            subLabel: (data[i.toString()].balance + ' ' + data[i.toString()].share + '%')
          })
          totalShare += data[i.toString()].share
        }
        pd.push({
          theta: (100 - totalShare) * 3.6 / 1.8 * Math.PI,
          label: 'Others',
          subLabel: ('N/A ' + (100 - totalShare).toFixed(2) + '%')
        })
        return pd
      })
      .then((pd) => {
        setGraphData(pd)
      })
      .then(() => {
        setLoading(false)
      })
      .catch((error) => {
        console.log(error)
      })
  }, [])

  const onNearestValue = (value) => {
    setValue({
      address: value.label,
      balance: value.subLabel.substring(0, value.subLabel.toString().indexOf(' ')),
      share: value.subLabel.substring(value.subLabel.toString().indexOf(' '), value.subLabel.toString().length)
    })
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
        <Container className="graphLayout">
          <Row>
            <div className="chartTitle">
              <h2>Top Token Holders</h2>
            </div>
          </Row>
          <Row>
            <div className="chartContainer">
              <FlexRadialChart
                className="pie-chart"
                innerRadius={40}
                radius={140}
                getAngle={d => d.theta}
                data={graphData}
                onValueMouseOver={onNearestValue}
                onSeriesMouseOut={() => setValue(false)}
                padAngle={0.04}
              >
              </FlexRadialChart>
            </div>
          </Row>
          <Col>
            <Table size="sm" style={{ color: currentTheme.foreground }}>
              <tbody>
                <tr>
                  <td className="statName">Address:</td>
                  <td className="statValue">{value.address}</td>
                </tr>
                <tr>
                  <td className="statName">Balance:</td>
                <td className="statValue">{value.balance}</td>
                </tr>
                <tr>
                  <td className="statName">Share:</td>
                  <td className="statValue">{value.share}</td>
                </tr>
              </tbody>
            </Table>
          </Col>
        </Container>
          )}
    </>
  )
}

function FearGreed () {
  const [graphData, setGraphData] = useState([])
  const [crosshairValues, setCrosshairValues] = useState([])
  const [loading, setLoading] = useState(true)
  const currentTheme = useSelector((state) => state.theme.currentTheme)

  const _onMouseLeave = () => {
    setCrosshairValues([])
  }

  const _onNearestX = (value) => {
    value.x = value.x.toString()
    setCrosshairValues([value])
  }

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_ROOT}/assets/historic-fear-greed`)
      .then((res) => {
        const data = JSON.parse(JSON.stringify(res.data))

        // get the first 30 historic fear and greed values
        const arr = data.crypto_values.slice(0, 30).map((d) => {
          return {
            x: d.timestamp,
            y: d.value,
            z: d.value_classification
          }
        })

        setGraphData(arr)
        setLoading(false)
      })
      .catch((error) => {
        console.log(`ERROR: ${error}`)
      })
  }, [])

  return (
    <div>
      <Container
        align="center"
        style={{
          background: currentTheme.background,
          color: currentTheme.foreground
        }}
      >
        {loading
          ? (
          <div>
            <Spinner animation="border" />
            <h4>Loading Crypto Fear and Greed Info...</h4>
          </div>
            )
          : (
          <div>
            <h3 style={{ color: currentTheme.foreground }}>
              Latest Crypto Fear and Greed Trends
            </h3>
            <FlexibleXYPlot
              onMouseLeave={_onMouseLeave}
              height={300}
              xType="ordinal"
            >
              <VerticalGridLines />
              <HorizontalGridLines />
              <XAxis
                hideTicks
                title="Latest 30 days"
                style={{ title: { fill: currentTheme.foreground } }}
              />
              <YAxis
                title="Fear Greed Index"
                style={{ title: { fill: currentTheme.foreground } }}
              />
              <LineSeries
                onNearestX={_onNearestX}
                data={graphData}
                color="blue"
              />
              <Crosshair
                values={crosshairValues}
                titleFormat={(d) => {
                  return { title: 'Date', value: d[0].x }
                }}
                itemsFormat={(d) => {
                  return [
                    { title: 'Index', value: d[0].y },
                    { title: 'Fear/Greed', value: d[0].z }
                  ]
                }}
              />
            </FlexibleXYPlot>
          </div>
            )}
      </Container>
    </div>
  )
}

function MentionsGraph (props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme)

  const [twitterData, setTwitterData] = useState([])
  const [redditData, setRedditData] = useState([])
  const [graphData, setGraphData] = useState({})

  const [loading, setLoading] = useState(true)
  const [crosshairValues, setCrosshairValues] = useState([])

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_ROOT}/assets/twitter_mentions_count`, {
        method: 'GET',
        params: {
          symbol: props.symbol
        }
      })
      .then((res) => {
        return JSON.parse(JSON.stringify(res.data))
      })
      .then((data) => {
        const points = []
        for (const key in data) {
          points.push({
            x: toUTC(data[key].end),
            y: data[key].tweet_count
          })
        }
        console.log(points)
        return points
      })
      .then((points) => {
        setTwitterData(points)
      })
      .catch((err) => {
        console.log(err)
      })
  }, [])

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_ROOT}/assets/reddit_mentions_count`, {
        method: 'GET',
        params: {
          symbol: props.symbol
        }
      })
      .then((res) => {
        return JSON.parse(JSON.stringify(res.data))
      })
      .then((data) => {
        const points = []
        for (const key in data) {
          points.push({
            x: toUTC(key),
            y: data[key]
          })
        }
        console.log(points)
        return points
      })
      .then((points) => {
        setRedditData(points)
      })
      .catch((err) => {
        console.log(err)
      })
  }, [])

  useEffect(() => {
    if (redditData.length > 0) {
      setGraphData({
        data: redditData,
        type: 'reddit',
        color: 'red'
      })
      setLoading(false)
      return
    }
    if (twitterData.length > 0) {
      setGraphData({
        data: twitterData,
        type: 'twitter',
        color: '#0d6efd'
      })
      setLoading(false)
    }
  }, [twitterData, redditData])

  const _onMouseLeave = () => {
    setCrosshairValues([])
  }

  const _onNearestX = (value) => {
    const x = value.x.toString()
    value.x = x
    setCrosshairValues([value])
  }

  const formatMentions = (data) => {
    return [{ title: 'mentions', value: data[0].y }]
  }

  const toUTC = (time) => {
    let date = new Date(time).toString()
    date = date.replace(' ', ', ')
    return date.substring(0, date.indexOf('-'))
  }

  return (
    <>
      { loading
        ? (
        <Container fluid>
          <Spinner animation="border" />
        </Container>
          )
        : (
        <Container className="graphLayout">
          <Row>
            <div className="chartTitle">
              <h2>Social Media Mentions</h2>
            </div>
          </Row>
          <Row>
            <div className="chartContainer">
              {(graphData.type === 'twitter' && twitterData.length === 0) ||
              (graphData.type === 'reddit' && redditData.length === 0)
                ? (
                    <Spinner animation="border" />
                  )
                : (
                  <FlexibleXYPlot
                    onMouseLeave={_onMouseLeave}
                    xType="ordinal"
                  >
                    <HorizontalGridLines />
                    {/* <VerticalGridLines/> */}

                    <LineSeries
                      animation={true}
                      data={graphData.data}
                      onNearestX={_onNearestX}
                      strokeWidth={2}
                      opacity={1}
                      color={graphData.color}
                    />

                    <Borders
                      style={{
                        bottom: { fill: currentTheme.fill },
                        left: { fill: currentTheme.fill },
                        right: { fill: currentTheme.fill },
                        top: { fill: currentTheme.fill }
                      }}
                    />

                    <YAxis />
                    <XAxis hideTicks />

                    <Crosshair
                      values={crosshairValues}
                      titleFormat={(d) => {
                        return { title: 'Date', value: d[0].x }
                      }}
                      itemsFormat={formatMentions}
                    />

                    <DiscreteColorLegend
                      orientation="horizontal"
                      style={{ position: 'absolute', right: '0%', top: '0%', backgroundColor: 'rgba(108,117,125, 0.7)', borderRadius: '5px' }}
                      items={[
                        {
                          title: 'Twitter',
                          color: '#0D6EFD',
                          strokeWidth: 5
                        },
                        {
                          title: 'Reddit',
                          color: 'red',
                          strokeWidth: 5
                        }
                      ]}
                    />
                  </FlexibleXYPlot>
                  )}
            </div>
          </Row>
          <Row>
            <Col>
              <ButtonGroup size="sm">
                <Button
                  variant="secondary"
                  className="redditToggle"
                  onClick={() => {
                    setGraphData({
                      data: redditData,
                      type: 'reddit',
                      color: 'red'
                    })
                  }}
                >
                  Reddit
                </Button>
                <Button
                  variant="secondary"
                  className="twitterToggle"
                  onClick={() => {
                    setGraphData({
                      data: twitterData,
                      type: 'twitter',
                      color: '#0d6efd'
                    })
                  }}
                >
                  Twitter
                </Button>
              </ButtonGroup>
            </Col>
          </Row>
        </Container>
          )}
    </>
  )
}

export {
  PriceVolumeGraph,
  SentimentGraph,
  TopTokenHolders,
  FearGreed,
  MentionsGraph
}
