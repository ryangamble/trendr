import React, { useState, useEffect } from "react";
import { Form, Row, Col, Button, Table} from "react-bootstrap";
import { useHistory } from "react-router-dom";
import axios from "axios";
import "./SearchBar.css";

function SearchBar() {
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
      history.push(`/result:${suggestions[0].symbol}`);
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
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      query: keyword
    }

    axios.post("/api/asset/search", requestBody)
    .then(res => {
      return JSON.parse(JSON.stringify(res.data.quotes));
    })
    .then(data => {
      var sg = [];
      console.log("autocomplete suggestions:");
      for(var key in data) {
        if (data[key].typeDisp === "Equity" || data[key].typeDisp === "Cryptocurrency" || data[key].typeDisp === "ETF") {
          sg.push({
            symbol: data[key].symbol,
            name: data[key].shortname,
            exchange: data[key].exchange,
            typeDisp: data[key].typeDisp
          })
        }
        console.log(data[key]);
      }
      return sg;
    })
    .then(sg => {
      setSuggestions(sg);
    })
    .catch(error => {
      console.log(error);
    });

    console.log("search keyword is:" + keyword);
  }, [keyword]);

  async function onSuggestionHandler(i) {
    console.log(suggestions[i].symbol)
    await (() => {
      setKeyword(suggestions[i].symbol);
      return;
    });
    setSuggestions([]);
    history.push(`/result:${suggestions[i].symbol}`); 
  }

  return (
    <div className="searchbar">
      <div className="searchbar__wrapper">
        <Row>
          <Col xs="12">
            <h2 className="searchbar__title fade-in-text">
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
            {suggestions && suggestions.map((suggestion, i) =>
              <Table hover size="sm" className="suggestions">
                <tbody>
                  <tr onClick={() => onSuggestionHandler(i)}>
                    <td className="suggestSymbol">{suggestion.symbol}</td>
                    <td className="suggestName">{suggestion.name}</td>
                  </tr>
                </tbody>
              </Table>
            )}
          </Col>

          <Col xs="5" md="3">
            <Button
              size="lg"
              className="searchbar__submit"
              variant="primary"
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
