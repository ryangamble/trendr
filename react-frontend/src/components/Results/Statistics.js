import React, { useEffect, useState } from "react";
import { Container, Image, Table, Col, Spinner } from "react-bootstrap";
import { useSelector } from "react-redux";
import axios from "axios";
import "./Results.css";

function Statistics(props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const [asset, setAsset] = useState({});
  const [link, setLink] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios
      .get("http://localhost:5000/assets/stats", {
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

        if (props.typeDisp === "etf" || props.typeDisp === "equity") {
          axios
            .get(`http://localhost:5000/assets/stocks/official-channels`, {
              method: "GET",
              params: {
                symbol: data["symbol"]
              }
            })
            .then((res) => {
              setLink(res.data["website"]);
            })
            .catch((error) => {
              console.log(error);
            });
        } else {
          axios
            .get(`http://localhost:5000/assets/cryptos/official-channels`, {
              method: "GET",
              params: {
                name: data["shortName"]
              }
            })
            .then((res) => {
              setLink(res.data["homepage"]);
            })
            .catch((error) => {
              console.log(error);
            });
        }
        setLoading(false);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  function formatPrice(num) {
    const options = {
      style: "currency",
      currency: asset.currency,
    };
    return num.toLocaleString("en-US", options);
  }

  function getNumberUnit(num) {
    let units = ["M", "B", "T", "Q"];
    let unit = Math.floor((num / 1.0e1).toFixed(0).toString().length);
    let r = unit % 3;
    let x = Math.abs(Number(num)) / Number("1.0e+" + (unit - r)).toFixed(2);
    return x.toFixed(2) + units[Math.floor(unit / 3) - 2];
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
          { link ?
              (<p>{link}</p>) :
              (<p> </p>)
          }
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
            </tbody>
          </Table>
        </Col>
      </Container>
    );
  }
}

export default Statistics;
