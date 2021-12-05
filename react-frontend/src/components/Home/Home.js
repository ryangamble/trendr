import React, { useEffect } from 'react'
import MyNavBar from '../NavBar/MyNavBar'
import SearchBar from '../SearchBar/SearchBar'

import { useSelector } from 'react-redux'
import { FearGreed } from '../Results/Graph'
import axios from 'axios'

function Home () {
  const currentTheme = useSelector((state) => state.theme.currentTheme)

  useEffect(() => {
    axios.post('http://localhost:5000/assets/populate_assets')
      .then(res => {
        console.log(res.data);
      }).catch(err => {
        console.log(err);
      });
  }, []);

  return (
    <div style={{ backgroundColor: currentTheme.background, height: '100vh' }}>
      <MyNavBar />
      <SearchBar />
      <FearGreed />
    </div>
  )
}

export default Home
