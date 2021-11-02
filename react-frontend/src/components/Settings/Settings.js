import React, { useEffect, useState } from "react";
// import React from "react";
import MyNavBar from "../NavBar/MyNavBar";
import axios from "axios";
import { toggleTheme } from "../Theme/themeActions";
import { Button } from "react-bootstrap";
import { useSelector, useDispatch } from "react-redux";

function Settings() {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  const currentUser = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(true);

  async function loadThemefromBackend() {
  //   (async () => {
  //     // GET request using axios with async/await
  //     const response = await axios.get("http://localhost:5000/users/test");
  //     console.log("\n\n\n\n");
  //     console.log(response);
  //     console.log("\n\n\n\n");
  //     return response;
  // })();
    axios
      .get("http://localhost:5000/users/test")
      .then(response => {return response})
      .catch(err => {console.log(err)});

    //     axios
  //       .get("http://localhost:5000/users/test", "test")
  //       .then((res) => {
  //         console.log("\n\n\n\n")
  //         console.log(res.data)
  //         console.log("\n\n\n\n")
  //         return JSON.stringify(res.data);
  //       }).catch( (error) => { alert(error) })
  //       // .then((data)=> {
  //       //   console.log(data)
  //       // })
  }
  // loadThemefromBackend();

  function storeThemetoBackend() {
  //   axios
  //   .get("http://localhost:5000/user/", "settings")
  //   .then((res) => {
  //     // console.log(res.data)
  //     return JSON.parse(JSON.stringify(res.data));
  //   })
  //   .then((data) => {
  //     console.log(data)
  //     return data;
  //   })

  }

  function storeThemeandToggle() {
    dispatch(toggleTheme());
    storeThemetoBackend();
  }

  return (
    <div style={{ backgroundColor: currentTheme.background }}>
      <MyNavBar />

      {/* {loadThemefromBackend().then( (res) => {
        console.log(res);
        return res;
      }
      )
      } */}
      {currentUser.username === "" && currentUser.email === ""
                  ? "You Must log in to save your settings!  "
                  // loadThemefromBackend()
                  : <Button variant={currentTheme.variant} >
                    Click the following button to save your theme settings
                    Test Button

                     </Button>

                    }

              <Button
                variant={currentTheme.variant}
                onClick={() => storeThemeandToggle()}
              >
                {currentTheme.name} Mode
        </Button>
    </div>
  );
}

export default Settings;
