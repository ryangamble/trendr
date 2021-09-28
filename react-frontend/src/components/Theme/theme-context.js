import React from "react";

export const themes = {
  light: {
    name: "Light",
    foreground: "#000000",
    background: "#eeeeee",
  },
  dark: {
    name: "Dark",
    foreground: "#ffffff",
    background: "#222222",
  },
};

export const ThemeContext = React.createContext(
  themes.light // default value
);
