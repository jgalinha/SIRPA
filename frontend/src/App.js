import { useContext } from "react";
import { Route, Switch, Redirect } from "react-router-dom";
import "./App.css";
import Header from "./components/Header";
import Navigation from "./components/UI/Navigation";
import Login from "./pages/Login";
import Today from "./pages/Today";
import UCs from "./pages/UCs";
import AuthContext from "./store/auth-context";
import { QueryClient, QueryClientProvider } from "react-query";

function App() {
  const authCtx = useContext(AuthContext);
  const queryClient = new QueryClient();
  queryClient.clear();

  return (
    <QueryClientProvider client={queryClient}>
      <Switch>
        {authCtx.isLoggedIn && (
          <>
            <Header />
            <Navigation />
            <Route path="/" exact>
              <Today />
            </Route>
            <Route path="/today" exact>
              <Today />
            </Route>
            <Route path="/ucs" exact>
              <UCs />
            </Route>
          </>
        )}
        {!authCtx.isLoggedIn && (
          <Route path="/login" exact>
            <Login />
          </Route>
        )}
        <Route path="*">
          <Redirect to="/login" exact />
        </Route>
      </Switch>
    </QueryClientProvider>
  );
}

export default App;
