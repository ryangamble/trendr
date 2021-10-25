import { initialThemeState, themeReducer } from "./themeActions";
import { initialUserState, userReducer } from "./userActions";

const redux = require("redux");
const createStore = redux.createStore;
const combineReducers = redux.combineReducers;

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
    if (
      JSON.parse(serializedStore).theme === undefined ||
      JSON.parse(serializedStore).user === undefined
    ) {
      console.log(serializedStore);
      console.log("theme is", JSON.parse(serializedStore).theme);
      throw new Error("local session store is corrupted");
    }
    return JSON.parse(serializedStore);
  } catch (e) {
    console.log(e);
    // return undefined;
    window.localStorage.setItem(
      "store",
      JSON.stringify({
        theme: { ...initialThemeState },
        user: { ...initialUserState },
      })
    );
    return { theme: { ...initialThemeState }, user: { ...initialUserState } };
  }
}

const persistedState = loadFromLocalStorage();

const rootReducer = combineReducers({
  theme: themeReducer,
  user: userReducer,
});

export const store = createStore(rootReducer, persistedState);

console.log("initial state", store.getState());

store.subscribe(() => console.log("updated state", store.getState()));

store.subscribe(() => saveToLocalStorage(store.getState()));