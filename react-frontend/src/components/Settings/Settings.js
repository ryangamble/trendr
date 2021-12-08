import React from 'react'
import MyNavBar from '../NavBar/MyNavBar'
import axios from 'axios'
import { toggleTheme } from '../Actions/themeActions'
import { updateCurrency } from '../Actions/currencyActions'
import { Row, Col, Form, FormCheck, Card, FloatingLabel } from 'react-bootstrap'
import { useSelector, useDispatch } from 'react-redux'

function Settings () {
  const currentTheme = useSelector((state) => state.theme.currentTheme)
  const currentCurrency = useSelector((state) => state.currency.currentCurrency)
  const currentUser = useSelector((state) => state.user)
  const dispatch = useDispatch()

  // todo replace theme with arbitrary json structure and have theme
  //  be just a single field. Also possibly have user class and settings
  //  be child class
  // function loadSettingsFromBackend () {
  //   if (currentUser.username === '' && currentUser.email === '') {
  //     axios
  //       .get(`${process.env.REACT_APP_API_ROOT}/users/settings`, { withCredentials: true })
  //       .then(response => {
  //         console.log('server: ' + response.data.dark_mode + '\nclient: ' + currentTheme.name)
  //         // false represents light, true represents dark
  //         if ((response.data.dark_mode === false && currentTheme.name === 'Dark') ||
  //           (response.data.dark_mode === true && currentTheme.name === 'Light')) {
  //           dispatch(toggleTheme())
  //         }
  //       })
  //       .catch(err => { console.log(err) })
  //   }
  // }

  function storeSettingsToBackend (currtheme, currcurrency) {
    if (currentUser.username !== '' || currentUser.email !== '') {
      axios
        .put(`${process.env.REACT_APP_API_ROOT}/users/settings`,
          {
            dark_mode: currtheme,
            currency: currcurrency
          },
          { withCredentials: true }
        )
        .then(response => {
          console.log('Saved theme: ' + (currtheme ? 'Dark' : 'Light'))
        })
        .catch(err => { console.log(err) })
    }
  }

  return (
    <div style={{
      background: currentTheme.background,
      color: currentTheme.foreground,
      height: '100vh'
    }}>
      <MyNavBar />
      <Row className="justify-content-md-center">
        <Col sm="12" md="6" lg="3">
          <Card>
            <Card.Header
              style={{ color: currentTheme.textColorLightBackground }}
            >
              Settings
            </Card.Header>
            <Card.Body>
              <Form>
                <Form.Group className="mb-3" controlId="formDarkMode">
                  <FormCheck
                    type="switch"
                    style={{
                      color: currentTheme.textColorLightBackground,
                      marginBottom: '50px'
                    }}
                    label= {currentTheme.name + ' Mode'}
                    variant={currentTheme.variant}
                    checked={(currentTheme.name === 'Dark')}
                    onChange={(e) => {
                      console.log(e)
                      // TODO: solve race condition better
                      storeSettingsToBackend(!(currentTheme.name === 'Dark'), currentCurrency)
                      dispatch(toggleTheme())
                    }}
                  />
                  <FloatingLabel controlId="floatingSelectCurrency" label="Currency" style={{
                    color: "#777"
                  }}>
                    <Form.Select
                        aria-label="Select Currency"
                        defaultValue={currentCurrency}
                        onChange={(e) => {
                          storeSettingsToBackend(currentTheme.name === 'Dark', e.target.value)
                          dispatch(updateCurrency(e.target.value))
                        }}
                    >
                      <option value="USD">USD</option>
                      <option value="EUR">EUR</option>
                      <option value="JPY">JPY</option>
                      <option value="GBP">GBP</option>
                      <option value="AUD">AUD</option>
                      <option value="CAD">CAD</option>
                      <option value="CHF">CHF</option>
                      <option value="CNY">CNY</option>
                      <option value="HKD">HKD</option>
                      <option value="NZD">NZD</option>
                      <option value="SEK">SEK</option>
                      <option value="KRW">KRW</option>
                      <option value="SGD">SGD</option>
                      <option value="NOK">NOK</option>
                      <option value="MXN">MXN</option>
                      <option value="INR">INR</option>
                      <option value="RUB">RUB</option>
                      <option value="ZAR">ZAR</option>
                      <option value="TRY">TRY</option>
                      <option value="BRL">BRL</option>
                      <option value="TWD">TWD</option>
                      <option value="DKK">DKK</option>
                      <option value="PLN">PLN</option>
                      <option value="THB">THB</option>
                      <option value="IDR">IDR</option>
                      <option value="HUF">HUF</option>
                      <option value="CZK">CZK</option>
                      <option value="ILS">ILS</option>
                      <option value="CLP">CLP</option>
                      <option value="PHP">PHP</option>
                      <option value="AED">AED</option>
                      <option value="COP">COP</option>
                      <option value="SAR">SAR</option>
                      <option value="MYR">MYR</option>
                      <option value="RON">RON</option>
                    </Form.Select>
                  </FloatingLabel>
                </Form.Group>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Settings
