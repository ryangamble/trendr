import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import PriceChart from "../Results/PriceChart";
import GeneralInfo from "../Results/GeneralInfo";

function Home() {
  return (
    <div>
      <MyNavBar />
      <GeneralInfo />
    </div>
  );
}

export default Home;
