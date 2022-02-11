import { useContext } from "react";
import { Route, Switch, Redirect } from "react-router-dom";
import "./App.css";
import Header from "./components/Header";
import Navigation from "./components/UI/Navigation";
import Login from "./pages/Login";
import Student from "./pages/Student";
import AuthContext from "./store/auth-context";

function App() {
  const authCtx = useContext(AuthContext);

  return (
    <Switch>
      {authCtx.isLoggedIn && (
        <>
          <Header />
          <Navigation />
          <Route path="/">
            <Student />
          </Route>
        </>
      )}
      {!authCtx.isLoggedIn && (
        <Route path="/login" exact>
          <Login />
        </Route>
      )}
      <Route path="*">
        <Redirect to="/login" />
      </Route>
    </Switch>
  );
}

export default App;
