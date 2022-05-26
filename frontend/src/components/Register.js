import { useRef, useState, useEffect } from "react";
import { faCheck, faTimes, faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import axios from 'axios';
//import AuthContext from "../context/AuthProvider";
import useAuth from "../hooks/useAuth";


//import qs from 'qs'

const REGISTER_URL = 'http://127.0.0.1:8000/token';

export default function Register(){
    
    const {setLogFlag, setAuth} = useAuth(); //useContext(AuthContext)
    const userRef = useRef();
    const errRef = useRef();
    const [user, setUser] = useState('');
    const [pwd, setPwd] = useState('');
    const [errMsg, setErrMsg] = useState('');
   
    //**** added 21.05 
    
const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('payload:');
    const headers = {'Content-Type': 'application/x-www-form-urlencoded'};
    const body  = JSON.stringify(`grant_type=&username=${user}&password=${pwd}&scope=&client_id=&client_secret=`);
    console.log(body);
    console.log('response :');
    try {
          await axios({ method:'post', 
                        url:  REGISTER_URL, 
                            headers: headers,
                            withCredentials: true, 
                            data: body
                    })
        .then(res => {
            console.log(res); 
            console.log(res.data);
            const accessToken = res?.data?.access_token;
            setAuth({user, pwd, accessToken});
            setLogFlag(true);
          });
        

    } catch (err) {
        console.log(err.response.status)
        if (!err.response) {
            setErrMsg('No Server Response');
        } else if (err.response.status === 402) {
            setErrMsg('Username Taken');
        } else {
            setErrMsg('Registration Failed')
        }
        errRef.current.focus();
    }
}

useEffect(() => {
        userRef.current.focus();
    }, [])

return (
<>
    <div ref={errRef}>{errMsg}</div>
    <h2> Please Login </h2>
    <form onSubmit={handleSubmit}>
        <div>
        <label htmlFor="username">
            Username:
            <FontAwesomeIcon icon={faCheck} className= "valid" />
            <input type="text" id="username" 
                onChange={(e) => setUser(e.target.value)}
                onClick ={(e)=> setErrMsg('')}
                value={user}
                ref={userRef}
            
            
            />    
        </label>
        </div>
        <div>
        <label htmlFor="password">
            Password:
            <FontAwesomeIcon icon={faCheck} className= "valid" />
            <input type="text" id="password" 
                onChange={(e) => setPwd(e.target.value)}
                value={pwd}
            
            
            />    
        </label>

        </div>

    <button >Sign Up</button>
    </form>
    </>
)
}

