import React from "react";
import { useHistory, useParams } from "react-router-dom";
import axios from "axios";

function ConfirmEmail() {
  const { confirmCode } = useParams();

  const history = useHistory();

  axios
    .post("http://localhost:5000/auth/confirm/" + confirmCode.substring(1))
    .then((res) => {
      history.push("/login");
    })
    .catch((error) => {
      alert(JSON.stringify(error.response.data.response.errors));
      history.push("/login");
    });

  return (<div><h1> </h1></div>);
}

export default ConfirmEmail;
