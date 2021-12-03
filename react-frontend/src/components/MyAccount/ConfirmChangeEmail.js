/* eslint-disable */
import React from 'react'
import { useHistory, useParams } from 'react-router-dom'
import axios from 'axios'

function ConfirmChangeEmail () {
  const { token } = useParams()

  const history = useHistory()

  const config = {
    headers: { "Content-Type": "application/json" },
    withCredentials: true,
    
  };

  console.log(token)

  axios
    .get('http://localhost:5000/users/confirm-change-email/' + token.substring(1), {}, config)
    .then((res) => {
        console.log(res)
    //   alert("Your new email has been confirmed and changed")
        history.push('/')
    })
    .catch((error) => {
      console.log(error)
    })

  return (<div><h1> </h1></div>)
}

export default ConfirmChangeEmail
