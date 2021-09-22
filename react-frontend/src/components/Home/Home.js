import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import PriceChart from "../Results/PriceChart";
import Statistics from "../Results/Statistics";

function Home() {
  return (
    <div>
      <MyNavBar />
      <Statistics />
    </div>
  );
}

export default Home;
