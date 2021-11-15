import React, { useState, useEffect } from "react";
import { Form, Row, Col, Button, Table } from "react-bootstrap";
import { useHistory } from "react-router-dom";
import { useSelector } from "react-redux";
import axios from "axios";
import "./SearchBar.css";

function SearchBar() {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  const [keyword, setKeyword] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const history = useHistory();

  const handleSearch = () => {
    if (keyword === "") {
      alert("Search field can not be empty!");
      return;
    }
    
    if (suggestions[0]) {
      var assetRoute = `/result/${suggestions[0].type}:${suggestions[0].id}`;
      if (suggestions[0].addr) {
        assetRoute += `:${suggestions[0].addr}`
      }
      history.push(assetRoute);
    } else {
      alert("No matching stocks or cryptos");
    }
  };

  useEffect(() => {
    if (keyword.length === 0) {
      setSuggestions([]);
      return;
    }

    axios
      .get("http://localhost:5000/assets/search", {
        method: "GET",
        params: {
          query: keyword,
        },
      })
      .then((res) => {
        let data = JSON.parse(JSON.stringify(res.data));
        var sg = [];
        console.log("autocomplete suggestions:");

        for (var key in data) {
          var ethAddr = "";
          if (data[key].typeDisp === "crypto") {
            if (typeof data[key]["platforms"]["ethereum"] != undefined) {
              ethAddr = data[key]["platforms"]["ethereum"];
            } else {
              ethAddr = null;
            }
          }
          sg.push({
            symbol: data[key].symbol,
            name: data[key].name,
            type: data[key].typeDisp,
            id:
              data[key].typeDisp === "crypto" ? data[key].id : data[key].symbol,
            addr: ethAddr,
          });
          // console.log(data[key]);
        }
        return sg;
      })
      .then((sg) => {
        console.log(sg);
        setSuggestions(sg);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [keyword]);

  async function onSuggestionHandler(i) {
    console.log(suggestions[i].symbol);
    await (() => {
      setKeyword(suggestions[i].symbol);
    });
    setSuggestions([]);
    var assetRoute = `/result/${suggestions[i].type}:${suggestions[i].id}`;
    if (suggestions[i].addr) {
      assetRoute += `:${suggestions[i].addr}`
    }
    history.push(assetRoute);
  }

  return (
    <div className="searchbar">
      <div className="searchbar__wrapper">
        <Row>
          <Col xs="12">
            <h2
              className="searchbar__title"
              style={{ color: currentTheme.foreground }}
            >
              Enter stock/cryptocurrency to see trends!
            </h2>
          </Col>
        </Row>
        <Row className="justify-content-md-center">
          <Col xs="7" md="9">
            <Form.Control
              size="lg"
              className="searchbar__input"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="Search for trends..."
            />
            {suggestions &&
              suggestions.map((suggestion, i) => (
                <Table hover size="sm" className="suggestions">
                  <tbody>
                    <tr onClick={() => onSuggestionHandler(i)}>
                      <td
                        className="suggestSymbol"
                        style={{ color: currentTheme.foreground }}
                      >
                        {suggestion.symbol}
                      </td>
                      <td
                        className="suggestName"
                        style={{ color: currentTheme.foreground }}
                      >
                        {suggestion.name}
                        {" - "}({suggestion.type.toUpperCase()})
                      </td>
                    </tr>
                  </tbody>
                </Table>
              ))}
          </Col>

          <Col xs="5" md="3">
            <Button
              size="lg"
              className="searchbar__submit"
              variant={currentTheme.variant}
              onClick={handleSearch}
            >
              Search
            </Button>
          </Col>
        </Row>
      </div>
    </div>
  );
}

export default SearchBar;
