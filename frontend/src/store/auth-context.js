import React, { useState, useEffect, useCallback } from "react";

let logoutTimer;

const AuthContext = React.createContext({
  token: "",
  isLoggedIn: false,
  userData: "",
  login: (token, userData) => {},
  logout: () => {},
});

const calculateExpirationTime = (exp) => {
  const currentTime = new Date().getTime();
  const expirationTime = new Date(exp * 1000);
  const remainingTime = expirationTime - currentTime;
  return remainingTime;
};

const getStoredData = () => {
  const initialToken = localStorage.getItem("token");
  const initialUserData = JSON.parse(localStorage.getItem("userData"));

  if (initialUserData && initialToken) {
    const remainingTime = calculateExpirationTime(initialUserData.exp);
    if (remainingTime <= 60000) {
      localStorage.removeItem("token");
      localStorage.removeItem("userData");
      return {
        token: null,
        userData: null,
      };
    }
  } else {
    return {
      token: null,
      userData: null,
    };
  }

  return {
    token: initialToken,
    userData: initialUserData,
  };
};

export const AuthContextProvider = (props) => {
  // FIXME: Change to cookies when in tls
  const storedData = getStoredData();

  const [token, setToken] = useState(storedData.token);
  const [userData, setUserData] = useState(storedData.userData);

  const userIsLoggedIn = !!token;

  const logoutHandler = useCallback(() => {
    setToken(null);
    setUserData(null);
    if (logoutTimer) {
      clearTimeout(logoutTimer);
    }
    // FIXME: Change to cookies when in tls
    localStorage.removeItem("token");
    localStorage.removeItem("userData");
  }, []);

  const loginHandler = (token, userData) => {
    setToken(token);
    setUserData(userData);
    // FIXME: Change to cookies when in tls
    localStorage.setItem("token", token);
    localStorage.setItem("userData", JSON.stringify(userData));
    // Handle auto logout
    logoutTimer = setTimeout(
      logoutHandler,
      calculateExpirationTime(userData.exp)
    );
  };

  useEffect(() => {
    if (token && userData) {
      logoutTimer = setTimeout(logoutHandler, userData.exp);
    }
  }, [token, userData, logoutHandler]);

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
