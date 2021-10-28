export const initialUserState = {
  username: "",
  email: "",
};

const USER_LOGIN = "USER_LOGIN";
const USER_LOGOUT = "USER_LOGOUT";

export const registerUser = (username, email) => {
  return {
    type: USER_LOGIN,
    payload: [username, email],
  };
};

export const removeUser = () => {
  return {
    type: USER_LOGOUT,
  };
};

export const userReducer = (state = initialUserState, action) => {
  switch (action.type) {
    case USER_LOGIN:
      return {
        ...state,
        username: action.payload[0],
        email: action.payload[1],
      };
    case USER_LOGOUT:
      return {
        ...state,
        username: "",
        email: "",
      };

    default:
      return {
        ...state,
      };
  }
};
