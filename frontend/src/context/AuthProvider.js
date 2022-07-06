import { createContext, useState } from 'react';

//a context creation with a provider
const AuthContext = createContext({});

//AUthProvider set around the App in Index.js
//every components of the App will have access
//to the context value auth. logflag (with
//their respective setters)
export const AuthProvider = ({children}) => {
    const [auth, setAuth] = useState({});
    const [logFlag, setLogFlag] = useState(false);
    return (
        <AuthContext.Provider value={{auth, setAuth, logFlag, setLogFlag}}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthContext;
  
