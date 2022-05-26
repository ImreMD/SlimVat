import {useContext} from 'react';
import AuthContext from '../context/AuthProvider';

// AuthContext = context object return from createContext
// will mark the context inside useContext
// current context value of the object is determined by 
// the nearest value  

const useAuth = () => {
    return useContext(AuthContext);
}

//returns the current value of the context object
export default useAuth;