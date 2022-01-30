import React, {useState} from 'react';
import Logo from '../../img/SIRPA_QR_Longo.svg'
import Button from '../UI/Button/Button';

const Login = (props) => {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const emailChangeHandler = e => {
        setEmail(e.target.value.trim())    
    }

    const passwordChangeHandler = e => {
        setPassword(e.target.value)
    }

    const submitHandler = e => {
        e.preventDefault();
        fetch("http://127.0.0.1:8000", {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        }).then(response => response.json().then(data => console.log(data)))
        setPassword("");
        setEmail("");
    }

    return (
        <div>
            <div className="min-h-screen bg-gray-100 flex flex-col justify-center sm:py-12">
                <div className="p-10 xs:p-0 mx-auto md:w-full md:max-w-md">
                    <div className='mb-5'>
                        <img src={Logo}></img>
                    </div>  
                    <div className="bg-white shadow w-full rounded-lg divide-y divide-gray-200">
                        <div className="px-5 py-7">
                            <form onSubmit={submitHandler}>                          
                                  <label className="font-semibold text-sm text-gray-600 pb-1 block">E-mail</label>
                                <input 
                                    type="email" 
                                    className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full"
                                    value={email}
                                    onChange={emailChangeHandler}
                                    required
                                />
                                <label className="font-semibold text-sm text-gray-600 pb-1 block">Password</label>
                                <input 
                                    type="password" 
                                    className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full" 
                                    value={password}
                                    onChange={passwordChangeHandler}
                                    required
                                />
                                <Button type="submit">
                                    <span className="inline-block mr-2">Login</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4 inline-block">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                    </svg>
                                </Button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;