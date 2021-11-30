import React from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'

import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css'

import Home from './components/Home/Home'
import Register from './components/Register/Register'
import Login from './components/Register/Login'
import Result from './components/Results/ResultsPage'
import Reset from './components/Register/Reset'
import SetPassword from './components/Register/SetPassword'
import ConfirmEmail from './components/Register/ConfirmEmail'
import About from './components/About/About'
import Settings from './components/Settings/Settings'
import { Provider } from 'react-redux'
import { store } from './components/Theme/store'
import MyAccount from './components/MyAccount/MyAccount'
import MyHistory from './components/MyAccount/MyHistory'
import ConfirmationPage from './components/Register/ConfirmationPage'

function App () {
  return (
    <Provider store={store}>
      <div className="App">
        <Router>
          <Switch>
            <Route path="/home" component={Home} />
            <Route path="/register" component={Register} />
            <Route path="/login" component={Login} />
            <Route path="/reset" component={Reset} />
            <Route path="/set-password:resetCode" component={SetPassword} />
            <Route path="/result/:id/" component={Result} />
            <Route path="/confirm-email:confirmCode" component={ConfirmEmail} />
            <Route path="/confirmation" component={ConfirmationPage} />
            <Route path="/myaccount" component={MyAccount} />
            <Route path="/history" component={MyHistory} />
            <Route path="/about" component={About} />
            <Route path="/settings" component={Settings} />
            <Route path="*" component={Home} />
          </Switch>
        </Router>
      </div>
    </Provider>
  )
}

export default App
