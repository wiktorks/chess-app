import React, { useState } from "react";

export const AuthContext = React.createContext({
  token: "",
  isLoggedIn: false,
  login: (token: string) => {},
  logout: () => {},
});

interface AuthContextProps {
  children: React.ReactNode;
}

const AuthContextProvider = (props: AuthContextProps) => {
  const [token, setToken] = useState("");

  const userIsLoggedIn = !!token;

  const loginHandler = (token: string) => {
    setToken(token);
  };
  const logoutHandler = () => {
    setToken("");
  };
  const contextValue = {
    token: token,
    isLoggedIn: userIsLoggedIn,
    login: loginHandler,
    logout: logoutHandler,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {props.children}
    </AuthContext.Provider>
  );
};

export { AuthContextProvider };
