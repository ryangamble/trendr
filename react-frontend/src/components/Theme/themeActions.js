export const themes = {
  light: {
    name: "Light",
    variant: "primary",
    foreground: "#000000",
    background: "#ffffff",
    linkColor: "#1976D2",
    textColorLightBackground: "black",
    fill: "#fff",
  },
  dark: {
    name: "Dark",
    variant: "secondary",
    foreground: "#ffffff",
    background: "#222222",
    linkColor: "#1976D2",
    textColorLightBackground: "black",
    fill: "#222",
  },
};

export const initialThemeState = {
  currentTheme: themes.light,
};

const TOGGLE_THEME = "TOGGLE_THEME";

export const toggleTheme = () => {
  return {
    type: TOGGLE_THEME,
    info: "toggle between light/dark modes",
  };
};

export const themeReducer = (state = initialThemeState, action) => {
  switch (action.type) {
    case TOGGLE_THEME:
      if (state.currentTheme.name === "Light") {
        return {
          ...state,
          currentTheme: themes.dark,
        };
      } else {
        return {
          ...state,
          currentTheme: themes.light,
        };
      }

    default:
      return {
        ...state,
      };
  }
};
