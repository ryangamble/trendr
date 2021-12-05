import React from 'react'
import MyNavBar from '../NavBar/MyNavBar'
import axios from 'axios'
import { toggleTheme } from '../Theme/themeActions'
import { Row, Col, Form, FormCheck, Card } from 'react-bootstrap'
import { useSelector, useDispatch } from 'react-redux'
import CurrencySelector from './CurrencySelector'

function Settings () {
  const currentTheme = useSelector((state) => state.theme.currentTheme)
  const currentUser = useSelector((state) => state.user)
  const dispatch = useDispatch()

  // todo replace theme with arbitrary json structure and have theme
  //  be just a single field. Also possibly have user class and settings
  //  be child class
  // function loadSettingsFromBackend () {
  //   if (currentUser.username === '' && currentUser.email === '') {
  //     axios
  //       .get('http://localhost:5000/users/settings', { withCredentials: true })
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

  function storeThemeToBackend (currtheme) {
    if (currentUser.username !== '' || currentUser.email !== '') {
      axios
        .put('http://localhost:5000/users/settings', { dark_mode: currtheme }, { withCredentials: true })
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
                    style={{ color: currentTheme.textColorLightBackground }}
                    label= {currentTheme.name + ' Mode'}
                    variant={currentTheme.variant}
                    checked={(currentTheme.name === 'Dark')}
                    onChange={(e) => {
                      console.log(e)
                      // TODO: solve race condition better
                      storeThemeToBackend(!(currentTheme.name === 'Dark'))
                      dispatch(toggleTheme())
                    }}
                  />
                </Form.Group>
              </Form>
              <CurrencySelector />
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Settings
