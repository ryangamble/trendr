import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import PriceChart from "./PriceChart";
import Statistics from "./Statistics";

function Home() {
  return (
    <div>
      <MyNavBar />
      <PriceChart symbol="AAPL"/>
      <Statistics />
    </div>
  );
}

export default Home;