import React, { useEffect, useState } from "react";
import {
  Container,
  Spinner,
  Row,
  Col,
  ButtonGroup,
  Button,
  Table
} from "react-bootstrap";

import { useSelector } from "react-redux";

import {
  XAxis,
  YAxis,
  HorizontalGridLines,
  VerticalGridLines,
  FlexibleXYPlot,
  RadialChart,
  LineSeries,
  MarkSeries,
  Crosshair,
  Borders,
  DiscreteColorLegend,
  makeVisFlexible
} from "react-vis";

import axios from "axios";
import "./Results.css";
import "../../../node_modules/react-vis/dist/style.css";

const FlexRadialChart = makeVisFlexible(RadialChart)

// Currently pass symbol as a prop, can be changed later
// Used for both price and volume charts for stocks
function StockGraph(props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const [graphData, setgraphData] = useState([]);

  const [min, setMin] = useState(0);
  const [max, setMax] = useState(0);
  const [loadedCount, setLoadedCount] = useState(0);
  const [crosshairValues, setCrosshairValues] = useState([]);
  const [period, setPeriod] = useState("1d");

  const periodDisplay = {
    "1d": "Past Day",
    "5d": "Past 5 Days",
    "1mo": "Past Month",
    "3mo": "Past 3 Months",
    "1y": "Past Year",
  };

  useEffect(() => {
    setLoadedCount(0);
    for (var key in periodDisplay) {
      console.log("fetching " + props.graphType + " data for " + key + "...");
      fetchDataPoints(key);
    }
  }, []);

  useEffect(() => {
    getMinMax();
    console.log("changing " + props.graphType + " period to " + period);
  }, [period, loadedCount]);

  async function fetchDataPoints(timePeriod) {

    axios
      .get("http://localhost:5000/assets/stock/history", {
        method: "GET",
        params: {
          symbol: props.symbol,
          period: timePeriod
        }
      })
      .then((res) => {
        return JSON.parse(JSON.stringify(res.data));
      })
      .then((data) => {
        var pd = [];
        var tableCol = "";
        if (props.graphType === "price") {
          tableCol = "Close";
        } else {
          tableCol = "Volume";
        }
        // console.log(data[tableCol])
        for (var key in data[tableCol]) {
          // console.log(key)
          // console.log(data['Close'][key].toFixed(2))
          var value = data[tableCol][parseInt(key)];
          if (typeof(value) != "number") {
            continue;
          }

          if (props.graphType === "price") {
            pd.push({
              x: unixToUTC(key),
              y: value.toFixed(2),
            });
          } else if (value > 0) {
            pd.push({
              x: unixToUTC(key),
              y: value,
            });
          }
        }
        return pd;
      })
      .then((pd) => {
        console.log(pd)
        var min = Number.MAX_VALUE;
        var max = 0;
        switch (timePeriod) {
          case "1d":
            setgraphData((prev) => ({ ...prev, "1d": pd }));
            break;
          case "5d":
            setgraphData((prev) => ({ ...prev, "5d": pd }));
            break;
          case "1mo":
            setgraphData((prev) => ({ ...prev, "1mo": pd }));
            break;
          case "3mo":
            setgraphData((prev) => ({ ...prev, "3mo": pd }));
            break;
          case "1y":
            setgraphData((prev) => ({ ...prev, "1y": pd }));
            break;
          default:
            setgraphData((prev) => ({ ...prev, "1d": pd }));
        }
        return [min, max];
      })
      .then(() => {
        console.log(props.graphType + " data loaded for " + timePeriod);
        setLoadedCount((prevCount) => prevCount + 1);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  function getMinMax() {
    var min = Number.MAX_VALUE;
    var max = 0;
    for (var key in graphData[period]) {
      var val = graphData[period][key].y;
      if (val > max) {
        max = val;
      }
      if (val < min) {
        min = val;
      }
    }
    setMin(min);
    setMax(max);
    // console.log(min);
  }

  const _onMouseLeave = () => {
    setCrosshairValues([]);
  };

  const _onNearestX = (value) => {
    var x = value.x.toString();
    value.x = x;
    setCrosshairValues([value]);
  };

  const itemsFormatPrice = (data) => {
    return [{ title: "price", value: formatPrice(data[0].y) }];
  };

  const itemsFormatVol = (data) => {
    return [{ title: "volume", value: data[0].y.toLocaleString("en-US") }];
  };

  const unixToUTC = (unix) => {
    var date = new Date(parseInt(unix)).toString();
    date = date.replace(" ", ", ");
    return date.substring(0, date.indexOf("-"));
  }

  const formatPrice = (num) => {
    if (num < 0.1) {
      return num.toFixed(7)
    }
    const options = {
      style: "currency",
      currency: props.currency
    };
    return num.toLocaleString("en-US", options);
  }

  return (
    <>
      {loadedCount < 5 ? (
        <Container fluid>
          <Spinner animation="border" />
        </Container>
      ) : (
        <Container className="graphLayout">
          <Row>
            <div className="chartTitle">
              {props.graphType === "price" ? (
                <h2>Price history</h2>
              ) : (
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
                  props.graphType === "price"
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
                  color={props.color}
                />
                <Borders
                  style={{
                    bottom: { fill: currentTheme.fill },
                    left: { fill: currentTheme.fill },
                    right: { fill: currentTheme.fill },
                    top: { fill: currentTheme.fill },
                  }}
                />

                <YAxis />
                <XAxis hideTicks />

                <Crosshair
                  values={crosshairValues}
                  itemsFormat={
                    props.graphType === "price"
                      ? itemsFormatPrice
                      : itemsFormatVol
                  }
                />
              </FlexibleXYPlot>
            </div>
          </Row>
          <Row>
            <Col>
              <ButtonGroup size="sm">
                <Button
                  variant="secondary"
                  className={props.graphType + "PeriodToggle"}
                  onClick={() => {
                    setPeriod("1d");
                  }}
                >
                  1D
                </Button>
                <Button
                  variant="secondary"
                  className={props.graphType + "PeriodToggle"}
                  onClick={() => setPeriod("5d")}
                >
                  5D
                </Button>
                <Button
                  variant="secondary"
                  className={props.graphType + "PeriodToggle"}
                  onClick={() => setPeriod("1mo")}
                >
                  1M
                </Button>
                <Button
                  variant="secondary"
                  className={props.graphType + "PeriodToggle"}
                  onClick={() => setPeriod("3mo")}
                >
                  3M
                </Button>
                <Button
                  variant="secondary"
                  className={props.graphType + "PeriodToggle"}
                  onClick={() => setPeriod("1y")}
                >
                  1Y
                </Button>
              </ButtonGroup>
            </Col>
            {props.graphType === "price" ? (
              <Col>
                {graphData[period][graphData[period].length - 1].y -
                  graphData[period][0].y >
                0 ? (
                  <div className="priceUp">
                    Up{" "}
                    {formatPrice(
                      graphData[period][graphData[period].length - 1].y -
                        graphData[period][0].y
                    )}{" "}
                    {periodDisplay[period]}
                  </div>
                ) : (
                  <div className="priceDown">
                    Down{" "}
                    {formatPrice(
                      graphData[period][graphData[period].length - 1].y -
                        graphData[period][0].y
                    )}{" "}
                    {periodDisplay[period]}
                  </div>
                )}
              </Col>
            ) : (
              <Col></Col>
            )}
          </Row>
        </Container>
      )}
    </>
  );
}

function CryptoGraph(props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const [graphData, setgraphData] = useState([]);

  const [min, setMin] = useState(0);
  const [max, setMax] = useState(0);
  const [loadedCount, setLoadedCount] = useState(0);
  const [crosshairValues, setCrosshairValues] = useState([]);
  const [period, setPeriod] = useState("1");

  const periodDisplay = {
    "1": "Past Day",
    "5": "Past 5 Days",
    "30": "Past Month",
    "90": "Past 3 Months",
    "365": "Past Year",
  };

  useEffect(() => {
    setLoadedCount(0);
    for (var key in periodDisplay) {
      console.log("fetching " + props.graphType + " data for " + key + "...");
      fetchDataPoints(key);
    }
  }, []);

  useEffect(() => {
    getMinMax();
    console.log("changing " + props.graphType + " period to " + period + " days");
  }, [period, loadedCount]);

  async function fetchDataPoints(timePeriod) {
    let apiRoute = "";
    if (props.graphType === "price") {
      apiRoute = "http://localhost:5000/assets/crypto/price-history";
    } else {
      apiRoute = "http://localhost:5000/assets/crypto/volume-history";
    }

    axios
      .get(apiRoute, {
        method: "GET",
        params: {
          id: props.symbol,
          days: timePeriod
        }
      })
      .then((res) => {
        return JSON.parse(JSON.stringify(res.data));
      })
      .then((data) => {
        var pd = []
        for (var i = 0; i < data.length; i++) {
          pd.push({
            x: data[i.toString()]['0'],
            y: parseFloat(data[i.toString()]['1'])
          })
        }
        return pd
      })
      .then((pd) => {
        console.log(pd)
        var min = Number.MAX_VALUE;
        var max = 0;
        switch (timePeriod) {
          case "1":
            setgraphData((prev) => ({ ...prev, "1": pd }));
            break;
          case "5":
            setgraphData((prev) => ({ ...prev, "5": pd }));
            break;
          case "30":
            setgraphData((prev) => ({ ...prev, "30": pd }));
            break;
          case "90":
            setgraphData((prev) => ({ ...prev, "90": pd }));
            break;
          case "365":
            setgraphData((prev) => ({ ...prev, "365": pd }));
            break;
          default:
            setgraphData((prev) => ({ ...prev, "1": pd }));
        }
        return [min, max];
      })
      .then(() => {
        console.log(props.graphType + " data loaded for " + timePeriod + " days");
        setLoadedCount((prevCount) => prevCount + 1);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  function getMinMax() {
    var min = Number.MAX_VALUE;
    var max = 0;
    for (var key in graphData[period]) {
      var val = graphData[period][key].y;
      if (val > max) {
        max = val;
      }
      if (val < min) {
        min = val;
      }
    }
    setMin(min);
    setMax(max);
    // console.log(min);
  }

  const _onMouseLeave = () => {
    setCrosshairValues([]);
  };

  const _onNearestX = (value) => {
    var x = value.x.toString();
    value.x = x;
    setCrosshairValues([value]);
  };

  const itemsFormatPrice = (data) => {
    return [{ title: "price", value: formatPrice(data[0].y) }];
  };

  const itemsFormatVol = (data) => {
    return [{ title: "volume", value: data[0].y.toLocaleString("en-US") }];
  };

  const formatPrice = (num) => {
    if (num < 0.1) {
      return "$" + num.toFixed(7).toString()
    }
    const options = {
      style: "currency",
      currency: "usd"
    };
    return num.toLocaleString("en-US", options);
  }


  return (
    <>
      {loadedCount < 5 ? (
        <Container fluid>
          <Spinner animation="border" />
        </Container>
      ) : (
        <Container className="graphLayout">
          <Row>
            <div className="chartTitle">
              {props.graphType === "price" ? (
                <h2>Price history</h2>
              ) : (
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
                  props.graphType === "price"
                    ? [0.98 * min, 1.02 * max]
                    : [0.9 * min, 1.2 * max]
                }
              >
                <HorizontalGridLines />
                {/* <VerticalGridLines /> */}

                <LineSeries
                  animation={true}
                  data={graphData[period]}
                  onNearestX={_onNearestX}
                  strokeWidth={2}
                  opacity={1}
                  color={props.color}
                />
                <Borders
                  style={{
                    bottom: { fill: currentTheme.fill },
                    left: { fill: currentTheme.fill },
                    right: { fill: currentTheme.fill },
                    top: { fill: currentTheme.fill },
                  }}
                />

                <YAxis />
                <XAxis hideTicks/>

                <Crosshair
                  values={crosshairValues}
                  itemsFormat={props.graphType === "price"
                  ? itemsFormatPrice
                  : itemsFormatVol
                  }
                />
              </FlexibleXYPlot>
            </div>
          </Row>
          <Row>
            <Col>
              <ButtonGroup size="sm">
                <Button
                  variant="secondary"
                  className={props.graphType + "PeriodToggle"}
                  onClick={() => {
                    setPeriod("1");
                  }}
                >
                  1D
                </Button>
                <Button
                  variant="secondary"
                  className={props.graphType + "PeriodToggle"}
                  onClick={() => setPeriod("5")}
                >
                  5D
                </Button>
                <Button
                  variant="secondary"
                  className={props.graphType + "PeriodToggle"}
                  onClick={() => setPeriod("30")}
                >
                  1M
                </Button>
                <Button
                  variant="secondary"
                  className={props.graphType + "PeriodToggle"}
                  onClick={() => setPeriod("90")}
                >
                  3M
                </Button>
                <Button
                  variant="secondary"
                  className={props.graphType + "PeriodToggle"}
                  onClick={() => setPeriod("365")}
                >
                  1Y
                </Button>
              </ButtonGroup>
            </Col>
            {props.graphType === "price" ? (
              <Col>
                {graphData[period][graphData[period].length - 1].y -
                  graphData[period][0].y >
                0 ? (
                  <div className="priceUp">
                    Up{" "}
                    {formatPrice(
                      graphData[period][graphData[period].length - 1].y -
                        graphData[period][0].y
                    )}{" "}
                    {periodDisplay[period]}
                  </div>
                ) : (
                  <div className="priceDown">
                    Down{" "}
                    {formatPrice(
                      graphData[period][graphData[period].length - 1].y -
                        graphData[period][0].y
                    )}{" "}
                    {periodDisplay[period]}
                  </div>
                )}
              </Col>
            ) : (
              <Col></Col>
            )}
          </Row>
        </Container>
      )}
    </>
  );
}

function SentimentGraph(props) {

  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const [twitterData, setTwitterData] = useState([]);
  const [redditData, setRedditData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect (() => {
    fetchTwitterData()
    fetchRedditData()
    setLoading(false);
  }, [props])

  // TODO: Make this fetch actual data
  function fetchRedditData(req) {
    var data = new Array(10).fill(0).reduce((prev,curr) =>
    [...prev, {
      x: Math.random() * 2 - 1,
      y: Math.random(),
      size: 1
    }], []);
      setRedditData(data);
  }

  function fetchTwitterData(req) {
    var data = new Array(10).fill(0).reduce((prev,curr) =>
    [...prev, {
      x: Math.random() * 2 - 1,
      y: Math.random(),
      size: 1
    }], []);
      setTwitterData(data);
  }

  // function fetchTwitterData() {
  //   axios
  //     .get("http://localhost:5000/assets/twitter_sentiment", {
  //       method: "GET",
  //       params: {
  //         symbol: props.symbol,
  //       }
  //     })
  //     .then((res) => {
  //       // console.log(res.data)
  //       return JSON.parse(JSON.stringify(res.data));
  //     })
  //     .then((data) => {
  //       // console.log(data['0']['1']['1'])
  //       var points = [];
  //       for (var i = 0; i < data.length; i++) {
  //         // console.log(data[i.toString()]['1'])
  //         points.push({
  //           x: parseFloat(data[i.toString()]['1']['0']),
  //           y: parseFloat(data[i.toString()]['1']['1']),
  //           size: 1,
  //         });
  //       }
  //       console.log("twitter sentiment analysis points")
  //       console.log(points)
  //       return points;
  //     })
  //     .then((points) => {
  //       return setTwitterData(points)
  //     })
  //     .then(()=> {
  //       setLoading(false)
  //     })
  // }

  const markSeriesProps = {
    animation: true,
    stroke: "grey",
    strokeWidth: 1,
    opacityType: "category",
    opacity: "0.4",
  }

  return (
    <>
      {loading ? (
        <Container fluid>
          <Spinner animation="border" />
        </Container>
      ) : (
        <Container className="graphLayout">
          <Row>
            <div className="chartTitle">
              <h2>Sentiment Data</h2>
            </div>
          </Row>
          {twitterData.length > 0 || redditData.legnth > 0 ?
            <Row>
              <div className="chartContainer">
                <FlexibleXYPlot
                  xDomain={[-1.0,1.0]}
                  yDomain={[0,1.0]}
                >

                  <HorizontalGridLines />
                  <VerticalGridLines />
                  <XAxis
                    title="Polarity"
                    style={{title: {fill: currentTheme.foreground}}}
                  />
                  <YAxis
                    title="Subjectivity"
                    style={{title: {fill: currentTheme.foreground}}}
                  />
                  <DiscreteColorLegend
                    orientation="horizontal"
                    style={{position: "absolute", right: "0%", top: "0%", backgroundColor: "rgba(108,117,125, 0.7)", borderRadius: "5px"}}
                    items={[
                      {
                        title: "Twitter",
                        color: "#0D6EFD",
                        strokeWidth: 5,
                      },
                      {
                        title: "Reddit",
                        color: "red",
                        strokeWidth: 5
                      }
                    ]}
                  />
                  <MarkSeries
                    {...markSeriesProps}
                    data={twitterData}
                    color="#0D6EFD"
                  />
                  <MarkSeries
                    {...markSeriesProps}
                    data={redditData}
                    color="red"
                  />
                </FlexibleXYPlot>
              </div>
            </Row>
          :
            <div>
              no data
            </div>
          }
        </Container>
      )}
    </>  
  );
}

function TopTokenHolders(props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const [graphData, setgraphData] = useState([]);
  const [value, setValue] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);

    axios
      .get("http://localhost:5000/assets/token/top-holders", {
        method: "GET",
        params: {
          address: props.addr
        }
      })
      .then((res) => {
        return JSON.parse(JSON.stringify(res.data));
      })
      .then((data) => {
        var pd = []
        var totalShare = 0;
        for (var i = 0; i < data.length; i++) {
          pd.push({
            theta: data[i.toString()]['share'] * 3.6 / 1.8 * Math.PI,
            label: data[i.toString()]['address'],
            subLabel: (data[i.toString()]['balance'] + " " + data[i.toString()]['share'] + "%")
          })
          totalShare += data[i.toString()]['share'];
        }
        pd.push({
          theta: (100 - totalShare) * 3.6 / 1.8 * Math.PI,
          label: "Others",
          subLabel: ("N/A " + (100 - totalShare).toFixed(2) + "%"),
        })
        return pd;
      })
      .then((pd) => {
        setgraphData(pd);
      })
      .then(() => {
        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
      });

  }, []);

  const onNearestValue = (value) => {
    setValue({
      address: value.label,
      balance: value.subLabel.substring(0, value.subLabel.toString().indexOf(" ")),
      share: value.subLabel.substring(value.subLabel.toString().indexOf(" "), value.subLabel.toString().length)
    });
  }
  
  return (
    <>
      {loading ? (
        <Container fluid>
          <Spinner animation="border" />
        </Container>
      ) : (
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
  );
}

function FearGreed() {
  const [graphData, setgraphData] = useState([]);
  const [crosshairValues, setCrosshairValues] = useState([]);
  const [loading, setLoading] = useState(true);
  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const _onMouseLeave = () => {
    setCrosshairValues([]);
  };

  const _onNearestX = (value) => {
    value.x = value.x.toString();
    setCrosshairValues([value]);
  };

  useEffect(() => {
    axios
      .get("http://localhost:5000/assets/historic-fear-greed")
      .then((res) => {
        let data = JSON.parse(JSON.stringify(res.data));

        // get the first 30 historic fear and greed values
        const arr = data["crypto_values"].slice(0, 30).map((d) => {
          return {
            x: d.timestamp,
            y: d.value,
            z: d.value_classification,
          };
        });

        setgraphData(arr);
        setLoading(false);
      })
      .catch((error) => {
        console.log(`ERROR: ${error}`);
      });
  }, []);

  return (
    <div>
      <Container
        align="center"
        style={{
          background: currentTheme.background,
          color: currentTheme.foreground,
        }}
      >
        {loading ? (
          <div>
            <Spinner animation="border" />
            <h4>Loading Crypto Fear and Greed Info...</h4>
          </div>
        ) : (
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
                style={{title: {fill: currentTheme.foreground}}}
              />
              <YAxis
                title="Fear Greed Index"
                style={{title: {fill: currentTheme.foreground}}}
              />
              <LineSeries
                onNearestX={_onNearestX}
                data={graphData}
                color="blue"
              />
              <Crosshair
                values={crosshairValues}
                titleFormat={(d) => {
                  return { title: "Date", value: d[0].x };
                }}
                itemsFormat={(d) => {
                  return [
                    { title: "Index", value: d[0].y },
                    { title: "Fear/Greed", value: d[0].z },
                  ];
                }}
              />
            </FlexibleXYPlot>
          </div>
        )}
      </Container>
    </div>
  );
}


export {
  StockGraph,
  CryptoGraph,
  SentimentGraph,
  TopTokenHolders,
  FearGreed
};
