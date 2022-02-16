import React, { useContext } from "react";
import AuthContext from "../store/auth-context";
import TodayStudent from "./TodayStudent";
import TodayTeacher from "./TodayTeacher";

const Today = () => {
  const authCtx = useContext(AuthContext);

  return (
    <>
      {authCtx.userData.isStudent && <TodayStudent />}
      {authCtx.userData.isTeacher && <TodayTeacher />}
    </>
  );
};

export default Today;
