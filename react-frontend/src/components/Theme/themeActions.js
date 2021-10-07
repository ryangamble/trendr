const redux = require("redux");
const createStore = redux.createStore;

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

function saveToLocalStorage(store) {
  try {
    const serializedStore = JSON.stringify(store);
    window.localStorage.setItem("store", serializedStore);
  } catch (e) {
    console.log(e);
  }
}

function loadFromLocalStorage() {
  try {
    const serializedStore = window.localStorage.getItem("store");
    if (serializedStore === null) return undefined;
    return JSON.parse(serializedStore);
  } catch (e) {
    console.log(e);
    // return undefined;
    window.localStorage.setItem("store", JSON.stringify(initialState));
    return initialState;
  }
}

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

const persistedState = loadFromLocalStorage();

export const store = createStore(reducer, persistedState);

console.log("initial state", store.getState());

store.subscribe(() => console.log("updated state", store.getState()));

store.subscribe(() => saveToLocalStorage(store.getState()));
