import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import SearchBar from "../SearchBar/SearchBar";

import { useSelector } from "react-redux";

function Home() {
  const currentTheme = useSelector((state) => state.theme.currentTheme);

  return (
    <div style={{ backgroundColor: currentTheme.background }}>
      <MyNavBar />
      <SearchBar />
    </div>
  );
}

export default Home;
