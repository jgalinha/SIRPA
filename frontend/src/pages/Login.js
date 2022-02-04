import React, {useState, useRef } from 'react';
import Logo from '../img/SIRPA_QR_Longo.svg'
import Button from '../components/UI/Button/Button';

const Login = (props) => {
    const emailInputRef = useRef();
    const passwordInputRef = useRef();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const emailChangeHandler = e => {
        setEmail(e.target.value)    
    }

    const passwordChangeHandler = e => {
        setPassword(e.target.value)
    }

    const submitHandler = e => {
        e.preventDefault()
        setIsLoading(true)
        // TODO Validation
        const enteredEmail = emailInputRef.current.value
        const enteredPassword = passwordInputRef.current.value

        fetch('http://127.0.0.1:8000/auth/login', {
            method: 'POST',
            body: new URLSearchParams({
                'username': enteredEmail,
                'password': enteredPassword,
                'grant_type': 'password',
            }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        }).then(res => {
            setIsLoading(false)
            if (res.ok) {
                return res.json().then((data) => {
                    console.log(data)
                })
            } else {
                return res.json().then((data) => {
                    console.log(data)
                })
            }
        })
    }

    return (
        <div>
            <div className="min-h-screen bg-gray-100 flex flex-col justify-center sm:py-12">
                <div className="p-10 xs:p-0 mx-auto md:w-full md:max-w-md">
                    <div className='mb-5'>
                        <img src={Logo} alt='SIRPA logo'></img>
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
                                    ref={emailInputRef}
                                    required
                                />
                                <label className="font-semibold text-sm text-gray-600 pb-1 block">Password</label>
                                <input 
                                    type="password" 
                                    className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full" 
                                    value={password}
                                    ref={passwordInputRef}
                                    onChange={passwordChangeHandler}
                                    required
                                />
                                <Button type="submit" disabled={isLoading}>
                                    {!isLoading &&
                                    <>
                                        <span className="inline-block mr-2">Login</span>
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4 inline-block">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                        </svg>
                                    </>}
                                    {isLoading && "..."}
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