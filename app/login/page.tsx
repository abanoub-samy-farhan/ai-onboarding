'use client';
import React, { useState } from 'react';
const LoginPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = (event: React.FormEvent) => {
        event.preventDefault();
        if (!password || !email) {
            setError('Please fill in all fields');
            return;
        }
        fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        }).then(async (res) => {
            const token = await res.json();
            if (!res.ok) {
                setError(token.error);
                return;
            }
            console.log(token.access_token_cookie);
            localStorage.setItem('access_token', token.access_token_cookie);
            window.location.href = '/profile';
        }).catch((err) => {
            console.error(err);
        })
        
    };

    return (
        <div className='flex flex-col items-center justify-center h-full'>
            <h1 className='text-4xl font-bold mb-5'>Login</h1>
            <form className='flex flex-col items-center gap-5 p-5 border border-gray-300 rounded-md'>
            <div className='flex flex-col gap-2'>
                <label>Email</label>
                <input
                    className='p-2 border border-gray-300 rounded-md focus:outline-none 
                    focus:ring-2 focus:ring-red-100 transition-all duration-100 ease-in-out'
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>
            <div className='flex flex-col gap-2'>
                <label>Password</label>
                <input
                    type="password"
                    className='p-2 border border-gray-300 rounded-md focus:outline-none
                    focus:ring-2 focus:ring-red-100 transition-all duration-100 ease-in-out'
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>
            <button className='border-2 rounded-lg w-fit px-10' onClick={handleLogin}>Login</button>
        </form>
        {/* Make other options of signing in */}
        <div className='flex flex-row items-center gap-5 mt-5'>
            <p>Or sign in with</p>
            <div className='flex gap-5'>
                <button className='border-2 rounded-lg w-fit px-10'>Google</button>
            </div>
        </div>
        {/* If user don't have account, sign up */}
        <div className='flex flex-row items-center gap-3 mt-5'>
            <p>Don't have an account?</p>
            <button className='text-blue-500 hover:text-blue-900 transition-all 
            duration-100 ease-in-out'
            onClick={() => window.location.href = '/signup'}>Sign Up</button>
        </div>
        {error && <p className='text-red-500 mt-5'>{error}</p>}
        </div>
    );
};

export default LoginPage;