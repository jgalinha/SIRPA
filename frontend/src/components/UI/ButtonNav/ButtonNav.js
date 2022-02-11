import React from "react";
import { NavLink } from "react-router-dom";
import styles from "./ButtonNav.module.css";

const ButtonNav = (props) => {
  return (
    <NavLink
      to={props.to}
      className={props.className || styles["btn-nav"]}
      onClick={props.onClick}
      disable={props.disabled}
      activeClassName={props.activeClassName}
      exact={props.exact || true}
    >
      {props.children}
    </NavLink>
  );
};

export default ButtonNav;
