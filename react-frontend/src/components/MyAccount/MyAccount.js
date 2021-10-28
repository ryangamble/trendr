import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import { useSelector } from "react-redux";

function MyAccount() {
  //color theme
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  //current user
  const currentUser = useSelector((state) => state.user);
  return (
    <div
      style={{
        backgroundColor: currentTheme.background,
        height: "100vh",
        color: currentTheme.foreground,
      }}
    >
      <MyNavBar />
      <p>
        Hello{" "}
        {currentUser.username === "" && currentUser.email === ""
          ? "Guest"
          : currentUser.email}
      </p>
    </div>
  );
}

export default MyAccount;
