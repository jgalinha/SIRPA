import React from "react";
import { Link } from "react-router-dom";
import styles from "./ButtonNav.module.css";

const ButtonNav = (props) => {
  return (
    <Link
      to={props.to}
      className={styles["btn-nav"] + " " + props.className}
      onClick={props.onClick}
      disable={props.disabled}
    >
      {props.children}
    </Link>
  );
};

export default ButtonNav;
