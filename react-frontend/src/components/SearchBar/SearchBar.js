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
    console.log("firing search to backend...");

    if (suggestions[0]) {
      history.push(`/result:${suggestions[0].type}/${suggestions[0].id}`);
    } else {
      alert("No matching stocks or cryptos");
      return;
    }
  };

  useEffect(() => {
    if (keyword.length === 0) {
      setSuggestions([]);
      return;
    }

    const requestBody = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      query: keyword,
    };

    axios
      .post("http://localhost:5000/assets/search", requestBody)
      .then((res) => {
        // console.log(res.data)
        return JSON.parse(JSON.stringify(res.data));
      })
      .then((data) => {
        var sg = [];
        console.log("autocomplete suggestions:");
        for (var key in data) {
          sg.push({
            symbol: data[key].symbol,
            name: data[key].name,
            type: data[key].typeDisp,
            id: data[key].typeDisp == "crypto" ? data[key].id : data[key].symbol
          });
          // console.log(data[key]);
        }
        return sg;
      })
      .then((sg) => {
        console.log(sg)
        setSuggestions(sg);
      })
      .catch((error) => {
        console.log(error);
      });

    console.log("search keyword is:" + keyword);
  }, [keyword]);

  async function onSuggestionHandler(i) {
    console.log(suggestions[i].symbol);
    await (() => {
      setKeyword(suggestions[i].symbol);
      return;
    });
    setSuggestions([]);
    history.push(`/result/${suggestions[i].type}/${suggestions[i].id}`);
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
                        {suggestion.name}{" "}
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
