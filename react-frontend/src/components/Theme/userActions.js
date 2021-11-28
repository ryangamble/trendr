export const initialUserState = {
  username: '',
  email: '',
  tempEmail: ''
}

const USER_LOGIN = 'USER_LOGIN'
const USER_LOGOUT = 'USER_LOGOUT'
const USER_CONFIRMATION = 'USER_CONFIRMATION'

export const registerUser = (username, email) => {
  return {
    type: USER_LOGIN,
    payload: [username, email]
  }
}

export const removeUser = () => {
  return {
    type: USER_LOGOUT
  }
}

// add a temporary email for confirmation page
export const registerConfirmation = (tempEmail) => {
  return {
    type: USER_CONFIRMATION,
    payload: [tempEmail]
  }
}

export const userReducer = (state = initialUserState, action) => {
  switch (action.type) {
    case USER_LOGIN:
      return {
        ...state,
        username: action.payload[0],
        email: action.payload[1]
      }
    case USER_LOGOUT:
      return {
        ...state,
        username: '',
        email: ''
      }

    case USER_CONFIRMATION:
      return {
        ...state,
        tempEmail: action.payload[0]
      }

    default:
      return {
        ...state
      }
  }
}
