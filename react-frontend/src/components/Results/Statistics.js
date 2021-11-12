import React, { useEffect, useState } from "react";
import { Container, Image, Table, Col, Spinner, OverlayTrigger, Tooltip } from "react-bootstrap";
import { useSelector } from "react-redux";
import axios from "axios";
import "./Results.css";

const getNumberUnit = (num) => {
  if (num < 1000000) {
    return num;
  }
  var units = ["M", "B", "T"];
  var unit = Math.floor((num / 1.0e1).toFixed(0).toString().length);
  var r = unit % 3;
  var x = Math.abs(Number(num)) / Number("1.0e+" + (unit - r)).toFixed(2);
  if (units[Math.floor(unit / 3) - 2] === undefined) {
    return Number.parseInt(num).toExponential(4);
  }
  return x.toFixed(2) + " " + units[Math.floor(unit / 3) - 2];
}

function StockStatistics(props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const [asset, setAsset] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios
      .get("http://localhost:5000/assets/stock/stats", {
        method: "GET",
        params: {
          symbol: props.symbol
        }
      })
      .then((res) => {
        let data = res.data;
        setAsset({
          companyName: data["longName"] ? data["longName"] : data["shortName"],
          logo: data["logo_url"],
          symbol: data["symbol"],
          currency: data["currency"] ? data["currency"] : "USD",
          dayOpen: data["open"],
          dayHigh: data["dayHigh"],
          dayLow: data["dayLow"],
          fiftyTwoWeekHigh: data["fiftyTwoWeekHigh"],
          fiftyTwoWeekLow: data["fiftyTwoWeekLow"],
          volume: data["volume"].toLocaleString("en-US"),
          avgVolume: data["averageVolume"].toLocaleString("en-US"),
          marketCap: data["marketCap"]
            ? getNumberUnit(data["marketCap"])
            : "N/A",
          pegRatio: data["pegRatio"] ? data["pegRatio"].toFixed(2) : "N/A",
          divYield: data["dividendYield"]
            ? (data["dividendYield"] * 100).toFixed(2)
            : "N/A",
        });
        props.currencyCallback(data["currency"]);

        axios
          .get(`http://localhost:5000/assets/stocks/official-channels`, {
            method: "GET",
            params: {
              symbol: props.symbol
            }
          })
          .then((res) => {
            // setLink(res.data["website"]);
            setAsset(prevData => { return {...prevData, website: res.data["website"]}})
          })
          .catch((error) => {
            console.log(error);
          });

        axios
          .get(`http://localhost:5000/assets/stocks/listed-exchanges`, {
            method: "GET",
            params: {
              symbol: props.symbol
            }
          })
          .then((res) => {
            console.log(res.data)
            setAsset(prevData => { return {...prevData, exchanges: res.data}})
          })
          .catch((error) => {
            console.log(error);
          });
      })
      .then(() => {
        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  function formatPrice(num) {
    if (num < 0.1) {
      return num.toFixed(7)
    }
    const options = {
      style: "currency",
      currency: "usd",
    };
    return num.toLocaleString("en-US", options);
  }

  function renderExchanges() {
    var list = [];
    for (var key in asset.exchanges.subarray(0, 2)) {
      list.push(<div>{asset.exchanges[key]}<br/></div>);
    }

    return (
      <div>
        {list}
        <OverlayTrigger
          placement="right"
          overlay={renderTooltip}
        >
          ...
        </OverlayTrigger>
      </div>
      
      );
  }

  function renderTooltip() {
    var list = [];
    for (var key in asset.exchanges.subarray(2, asset.exchanges.length)) {
      list.push(<div>{asset.exchanges[key]}<br/></div>);
    }
    return(
      <Tooltip>
        {list}
      </Tooltip>
    );
  }

  if (loading) {
    return (
      <Container fluid>
        <Spinner animation="border" />
      </Container>
    );
  } else {
    return (
      <Container fluid>
        <Col>
          <Image src={asset.logo} rounded />
          <h2>{asset.companyName}</h2>
          <p>{asset.symbol}</p>
          { asset.website && <a href={asset.website} target="_blank">Homepage</a>}
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
                <td className="statValue">{renderExchanges()}</td>
              </tr>
            </tbody>
          </Table>
        </Col>
      </Container>
    );
  }
}

function CoinStatistics(props) {

  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const [crypto, setCrypto] = useState([]);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    setLoading(true);
    axios
      .get("http://localhost:5000/assets/crypto/stats", {
        method: "GET",
        params: {
          id: props.id
        }
      })
      .then((res) => {
        let data = res.data;
        console.log(data);
        setCrypto(data);
        axios
          .get(`http://localhost:5000/assets/cryptos/official-channels`, {
            method: "GET",
            params: {
              id: props.id
            }
          })
          .then((res) => {
            setCrypto(prevData => { return {...prevData, website: res.data["homepage"]}});
          })
          .catch((error) => {
            console.log(error);
          });

        axios
          .get(`http://localhost:5000/assets/cryptos/listed-exchanges`, {
            method: "GET",
            params: {
              id: props.id
            }
          })
          .then((res) => {
            console.log(res.data)
            setCrypto(prevData => { return {...prevData, exchanges: res.data}})
          })
          .catch((error) => {
            console.log(error);
          });
      })
      .then(() => {
        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  function formatPrice(num) {
    if (num < 0.1) {
      return "$" + num.toFixed(7).toString()
    }
    const options = {
      style: "currency",
      currency: "usd",
    };
    return num.toLocaleString("en-US", options);
  }

  function renderExchanges() {
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
      
      );
  }

  function renderTooltip() {
    var list = [];
    for (var key in crypto.exchanges) {
      list.push(crypto.exchanges[key] + ", ");
    }
    list[list.length - 1] = list[list.length - 1].substring(0, list[list.length - 1].lastIndexOf(","))
    return(
      <Tooltip>
        {list}
      </Tooltip>
    );
  }

  if (loading) {
    return (
      <Container fluid>
        <Spinner animation="border" />
      </Container>
    );
  } else {
    return(
      <Container fluid>
        <Col>
        <Col>
          <Image src={crypto.Image} rounded />
          <h2>{crypto.Name}</h2>
          <p>{crypto.Symbol.toUpperCase()}</p>
          {crypto.website && <a href={crypto.website} target="_blank">Homepage</a>}
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
                <td className="statValue">{formatPrice(crypto['DayHigh'])}</td>
              </tr>
              <tr>
                <td className="statName">Day Low</td>
                <td className="statValue">{formatPrice(crypto['DayLow'])}</td>
              </tr>
              <tr>
                <td className="statName">Market Cap Rank</td>
                <td className="statValue">{crypto['MarketCapRank'] ? crypto['MarketCapRank'] : "N/A"}</td>
              </tr>
              <tr>
                <td className="statName">24 Hour Volume</td>
                <td className="statValue">{crypto['24HrVolume']}</td>
              </tr>
              <tr>
                <td className="statName">24 Hour Change</td>
                <td className="statValue">{crypto['24HrChange']}</td>
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
    );
  }
}

function TokenStatistics(props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const [token, setToken] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // console.log(props.addr)
    setLoading(true);
    axios
      .get("http://localhost:5000/assets/token/info", {
        method: "GET",
        params: {
          address: props.addr
        }
      })
      .then((res) => {
        setLoading(true);
        return JSON.parse(JSON.stringify(res.data));
      })
      .then((data) => {
        console.log(data);
        setToken(data);
      })
      .then(() => {
        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  if (loading) {
    return (
      <Container fluid>
        <Spinner animation="border" />
      </Container>
    );
  } else {
    return(
      <Container fluid>
        <Col>
          <h2 style={{textAlign: "left"}}>Token Info</h2>
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
    );
  }
}

export {
  StockStatistics,
  CoinStatistics,
  TokenStatistics
};
