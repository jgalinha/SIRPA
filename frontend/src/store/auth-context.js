import React, { useState } from "react";

const AuthContext = React.createContext({
  token: "",
  isLoggedIn: false,
  userData: "",
  login: (token, userData) => {},
  logout: () => {},
});

export const AuthContextProvider = (props) => {
  const [token, setToken] = useState(null);
  const [userData, setUserData] = useState(null);

  const userIsLoggedIn = !!token;

  const loginHandler = (token, userData) => {
    setToken(token);
    setUserData(userData);
  };

  const logoutHandler = () => {
    setToken(null);
    setUserData(null);
  };

  const contextValue = {
    token: token,
    isLoggedIn: userIsLoggedIn,
    userData: userData,
    login: loginHandler,
    logout: logoutHandler,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
