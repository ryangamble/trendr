import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import SearchBar from "../SearchBar/SearchBar";

import { useSelector } from "react-redux";

function Home() {
  const currentTheme = useSelector((state) => state.currentTheme);

  return (
    <div style={{ "background-color": currentTheme.background }}>
      <MyNavBar />
      <SearchBar />
    </div>
  );
}

export default Home;
