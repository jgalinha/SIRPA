import React, { useContext, useState, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import Logo from "../img/SIRPA.svg";
import AuthContext from "../store/auth-context";
import BurgerMenu from "./UI/BurgerMenu";
import { UserIcon } from "@heroicons/react/outline";

const Header = () => {
  const authCtx = useContext(AuthContext);
  const [username, setUsername] = useState();
  const isLoggedIn = authCtx.isLoggedIn;

  const logoutHandler = useCallback(() => {
    setUsername("");
    authCtx.logout();
  }, [authCtx]);

  useEffect(() => {
    if (isLoggedIn && authCtx.userData !== null) {
      setUsername(authCtx.userData.username);
    }
  }, [isLoggedIn, authCtx, logoutHandler]);

  return (
    <>
      <header className="border-b-2 border-gray-200">
        <div className="p-1 mx-auto flex max-w-7xl items-center justify-between md:p-4">
          <div className="flex items-center">
            <BurgerMenu />
            <Link to="/" className="mr-2">
              <img
                src={Logo}
                alt="SIRPA Logo"
                className=" min-w-fit min-h-fit"
              />
            </Link>
            <p className="invisible xl:text-xl xl:visible max-w-xs font-sans font-medium">
              Sistema Integrado de Resgisto de Presenças em Aula
            </p>
          </div>
          {isLoggedIn && (
            <nav className="flex items-center space-x-1 text-sm font-medium text-gray-800">
              <Link
                to="/me"
                className="inline-flex items-center rounded px-4 py-2 bg-gray-400 transition hover:bg-gray-600 hover:text-white"
              >
                <UserIcon className="flex mr-2 p-0 w-5 h-5" />
                <span>{username}</span>
              </Link>
              <button
                onClick={logoutHandler}
                className="bg-red-600 rounded px-4 py-2 text-white transition hover:bg-red-700"
              >
                logout
              </button>
            </nav>
          )}
          {!isLoggedIn && (
            <nav className="flex items-center space-x-1 text-sm font-medium text-gray-800">
              <Link
                to="/login"
                className="bg-red-600 rounded px-4 py-2 text-white transition hover:bg-red-700"
              >
                Login
              </Link>
            </nav>
          )}
        </div>
      </header>
    </>
  );
};

export default Header;
