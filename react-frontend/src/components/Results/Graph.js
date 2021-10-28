import React, { useEffect, useState } from "react";
import {
  Container,
  Spinner,
  Row,
  Col,
  ButtonGroup,
  Button,
} from "react-bootstrap";

import { useSelector } from "react-redux";

import {
  XAxis,
  YAxis,
  HorizontalGridLines,
  VerticalGridLines,
  FlexibleXYPlot,
  LineSeries,
  MarkSeries,
  Crosshair,
  Borders,
  DiscreteColorLegend,
  Hint,
} from "react-vis";

import axios from "axios";
import "./Results.css";
import "../../../node_modules/react-vis/dist/style.css";

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
    const requestBody = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      name: props.symbol,
      period: timePeriod,
    };

    axios
      .post("http://localhost:5000/assets/history", requestBody)
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
        for (var key in data[tableCol]) {
          // console.log(key)
          // console.log(data['Close'][key].toFixed(2))
          var value = data[tableCol][key];
          if (props.graphType === "price") {
            pd.push({
              x: new Date(parseInt(key)),
              y: value,
            });
          } else if (value > 0) {
            pd.push({
              x: new Date(parseInt(key)),
              y: value,
            });
          }
        }
        return pd;
      })
      .then((pd) => {
        // console.log(pd)
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
        console.log(props.graphType + " data loaded for " + requestBody.period);
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

  function formatPrice(num) {
    const options = {
      style: "currency",
      currency: props.currency,
    };
    return num.toLocaleString("en-US", options);
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

  if (loadedCount < 5) {
    return (
      <Container fluid>
        <Spinner animation="border" />
      </Container>
    );
  } else {
    return (
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
    );
  }
}


export default Graph;


function SentimentGraph(props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const [twitterData, setTwitterData] = useState([]);
  const [redditData, setRedditData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect (() => {
    const requestBody = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      name: props.symbol,
    };

    fetchTwitterData(requestBody)
    fetchRedditData(requestBody)

  }, [props])

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
    axios
      .post("http://localhost:5000/assets/twitter_sentiment", req)
      .then((res) => {
        // console.log(res.data)
        return JSON.parse(JSON.stringify(res.data));
      })
      .then((data) => {
        // console.log(data['0']['1']['1'])
        var points = [];
        for (var i = 0; i < data.length; i++) {
          // console.log(data[i.toString()]['1'])
          points.push({
            x: parseFloat(data[i.toString()]['1']['0']),
            y: parseFloat(data[i.toString()]['1']['1']),
            size: 1,
          });
        }
        console.log("twitter sentiment analysis points")
        console.log(points)
        return points;
      })
      .then((points) => {
        return setTwitterData(points)
      })
      .then(()=> {
        setLoading(false)
      })
  }

  const markSeriesProps = {
    animation: true,
    stroke: "grey",
    strokeWidth: 1,
    opacityType: "category",
    opacity: "0.4",
  }

  if (loading) {
    return (
      <Container fluid>
        <Spinner animation="border" />
      </Container>
    );
  } else {
    return (
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
    );
  }
}

// Need separate functions for price/volume charts for cryptos

export {
  StockGraph,
  SentimentGraph
};