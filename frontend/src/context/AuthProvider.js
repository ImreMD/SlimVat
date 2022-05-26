import { createContext, useState } from 'react';

//a context creation with a provider
const AuthContext = createContext({});


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
  
