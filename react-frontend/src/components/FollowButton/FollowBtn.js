import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'

import { Button } from 'react-bootstrap'
import axios from 'axios'

// A reusable follow botton component that takes the stock/crypto id as props

function FollowBtn ({ id, isFollow, callback }) {
  const currentTheme = useSelector((state) => state.theme.currentTheme)
  // current user
  const currentUser = useSelector((state) => state.user)
  // a followed flag to indicate whether the current user follows the stock/crypto
  const [followed, setFollowed] = useState(false)

  useEffect(() => {
    // do this only if user is logged in
    if (currentUser.email !== '' || currentUser.username !== '') {
      setFollowed(isFollow)
    }
  }, [isFollow])

  const handleFollow = (e) => {
    e.preventDefault()

    const json = JSON.stringify({
      id: id
    })
    const config = {
      headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: true
    }

    // send follow/unfollow request to backend
    if (followed) {
      console.log('Unfollowing ', id)
      axios
        .post(`/api/users/unfollow-asset`, json, config)
        .then((res) => {
          console.log(res)
          if (res.status === 200 && res.data.success === true) {
            // toggle between follow/unfollow
            setFollowed(!followed)
          } else {
            alert('Error following!')
          }
        })
        .catch((error) => {
          alert(JSON.stringify(error.response.data.response.errors))
        })

      if (callback) {
        callback(id)
      }
    } else {
      console.log('Following ', id)
      axios
        .post(`/api/users/follow-asset`, json, config)
        .then((res) => {
          if (res.status === 200 && res.data.success === true) {
            // toggle between follow/unfollow
            setFollowed(!followed)
          } else {
            alert('Error following!')
          }
          console.log(res)
        })
        .catch((error) => {
          alert(JSON.stringify(error.response.data.response.errors))
        })
    }
  }

  useEffect(() => {
    // If the user is not logged in, return
    if (currentUser.username === '' && currentUser.email === '') return

    // First Page Initial Mount, fetch whether the user follows this stock/crypto
    console.log(
      'fetching from backend to see whether the user follows this stock...',
      id
    )
  }, [])

  return (
    <div>
      <Button variant={currentTheme.variant} onClick={handleFollow}>
        {followed ? 'Unfollow' : 'Follow'}
      </Button>
    </div>
  )
}

export default FollowBtn
