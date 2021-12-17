import { Switch, Route, Redirect } from "react-router-dom";
import { useContext } from "react";

import { AuthContext } from "./store/auth-context";
import { Layout } from "./components/Layout/Layout";
import { AuthPage } from "./pages/AuthPage";
import { ProfilePage } from "./pages/ProfilePage";
import { HomePage } from "./pages/HomePage";

const App = () => {
  const authCtx = useContext(AuthContext);

  return (
    <Layout>
      <Switch>
        <Route path="/" exact>
          <HomePage />
        </Route>
        {authCtx.isLoggedIn ? (
          <>
            <Route path="/profile">
              <ProfilePage />
            </Route>
            <Route path="/game">
              {/* <GamePage /> */}
            </Route>
          </>
        ) : (
          <Route path="/auth">
            <AuthPage />
          </Route>
        )}
        <Route path='*'>
          <Redirect to='/'></Redirect>
        </Route>
      </Switch>
    </Layout>
  );
};

export default App;
