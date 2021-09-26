import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

import Home from "./components/Home/Home";
import Register from "./components/Register/Register";
import Login from "./components/Register/Login";

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/home" component={Home}></Route>
          <Route path="/register" component={Register}></Route>
          <Route path="/login" component={Login}></Route>

          <Route path="*" component={Home}></Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
