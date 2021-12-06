import React, { useEffect } from 'react'
import MyNavBar from '../NavBar/MyNavBar'
import SearchBar from '../SearchBar/SearchBar'

import { useSelector } from 'react-redux'
import { FearGreed } from '../Results/Graph'
import axios from 'axios'

function Home () {
  const currentTheme = useSelector((state) => state.theme.currentTheme)

  return (
    <div style={{ backgroundColor: currentTheme.background, height: '100vh' }}>
      <MyNavBar />
      <SearchBar />
      <FearGreed />
    </div>
  )
}

export default Home
