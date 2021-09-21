import React from "react";
import {Container} from "react-bootstrap";
import TradingViewWidget, {Themes, BarStyles} from "react-tradingview-widget";

// Currently pass symbol as a prop, can be changed later
function PriceChart(props) {
  return(
    <Container fluid>
      <TradingViewWidget
        symbol={props.symbol}
        theme={Themes.LIGHT}
        style={BarStyles.AREA}
        save_image={false}
        interval="D"
        locale="en"
        enable_publishing={false}
      />
    </Container>
  );
}

export default PriceChart;