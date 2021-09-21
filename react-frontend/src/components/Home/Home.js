import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import PriceChart from "../Results/PriceChart";

function Home() {
  return (
    <div>
      <MyNavBar />
      <PriceChart symbol="BINANCE:BTCUSDT" />
    </div>
  );
}

export default Home;
