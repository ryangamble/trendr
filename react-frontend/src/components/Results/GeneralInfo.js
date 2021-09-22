import React, { useEffect, useState } from "react";
import {Container} from "react-bootstrap";
import axios from "axios";
import "./Results.css"

function GeneralInfo() {
  
  const [stock, setStock] = useState();

  const requestBody = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json'},
    name: 'AAPL'
  }

  useEffect(() => {
    axios.post('http://127.0.0.1:5000/result/general', requestBody)
      .then(res => {
        setStock(res.data);
      });
  }, []);
  
  return (
    <Container fluid>
      <div className="generalInfoContainer">
        {JSON.stringify(stock)}
      </div>
    </Container>
  );
}

export default GeneralInfo