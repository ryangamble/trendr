import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

import Home from "./components/Home/Home";
import Register from "./components/Register/Register";
import Login from "./components/Register/Login";
import Result from "./components/Results/ResultsPage";

import { Provider } from "react-redux";
import { store } from "./components/Theme/themeActions";

function App() {
  return (
    <Provider store={store}>
      <div className="App">
        <Router>
          <Switch>
            <Route path="/home" component={Home}></Route>

            <Route path="/signup" component={Register}></Route>
            <Route path="/login" component={Login}></Route>

            <Route path="/result:id" component={Result}></Route>

            <Route path="*" component={Home}></Route>
          </Switch>
        </Router>
      </div>
    </Provider>
  );
}

export default App;
