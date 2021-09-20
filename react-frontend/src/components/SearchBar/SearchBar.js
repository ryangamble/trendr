import React, { useState, useEffect } from "react";
import { Form, Row, Col, Button } from "react-bootstrap";
import { useHistory } from "react-router-dom";

import "./SearchBar.css";

function SearchBar() {
  const [keyword, setKeyword] = useState("");
  const history = useHistory();

  const handleSearch = () => {
    if (keyword === "") {
      alert("Search field can not be empty!");
      return;
    }
    console.log("firing search to backend...");
    history.push(`/result:${keyword}`);
  };

  useEffect(() => {
    console.log("search keyword is:" + keyword);
  }, [keyword]);
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
          <Col xs="9">
            <Form.Control
              size="lg"
              className="searchbar__input"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              autoFocus
              placeholder="Search for trends..."
            />
          </Col>

          <Col xs="3">
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
