const redux = require("redux");
const createStore = redux.createStore;

export const themes = {
  light: {
    name: "Light",
    variant: "primary",
    foreground: "#000000",
    background: "#ffffff",
    linkColor: "#1976D2",
    fill: "#fff",
  },
  dark: {
    name: "Dark",
    variant: "secondary",
    foreground: "#ffffff",
    background: "#222222",
    linkColor: "white",
    fill: "#222",
  },
};

const initialState = {
  currentTheme: themes.light,
};

const TOGGLE_THEME = "TOGGLE_THEME";

export const toggleTheme = () => {
  return {
    type: TOGGLE_THEME,
    info: "toggle between light/dark modes",
  };
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case TOGGLE_THEME:
      if (state.currentTheme === themes.light) {
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

export const store = createStore(reducer);

console.log("initial state", store.getState());

store.subscribe(() => console.log("updated state", store.getState()));
