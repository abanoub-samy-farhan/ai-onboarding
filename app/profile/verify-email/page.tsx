'use client'
import { stringify } from 'querystring';
import React, { useState, useEffect } from 'react';

const VerifyEmailPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [verificationCode, setVerificationCode] = useState('');
    const [isVerified, setIsVerified] = useState(false);
    const [isResendDisabled, setIsResendDisabled] = useState(false);
    const [countdown, setCountdown] = useState(0);

    useEffect(() => {
        // Check if there was a countdown before
        const storedTimestamp = localStorage.getItem('resendTimer');
        if (storedTimestamp) {
            const remainingTime = Math.max(0, 60 - Math.floor((Date.now() - parseInt(storedTimestamp)) / 1000));
            if (remainingTime > 0) {
                setIsResendDisabled(true);
                setCountdown(remainingTime);
                startCountdown(remainingTime);
            }
        }
    }, []);

    const startCountdown = (time: number) => {
        const timer = setInterval(() => {
            setCountdown((prev) => {
                if (prev <= 1) {
                    clearInterval(timer);
                    setIsResendDisabled(false);
                    localStorage.removeItem('resendTimer'); // Clear localStorage after countdown ends
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
    };

    const handleResendVerification = () => {
        // Disable the button and start countdown
        setIsResendDisabled(true);
        setCountdown(60);
        localStorage.setItem('resendTimer', Date.now().toString()); // Store timestamp
        startCountdown(60);
        fetch('http://localhost:5000/api/v1/auth/generate/otp', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        }).then(async (res) => {
            if (!res.ok){
                console.log(await res.json());
            }
        })

        // Simulate sending a verification token
        console.log("Verification token sent to user!");
    };

    const handleVerification = () => {
      if (!verificationCode){
        alert("Please enter the verification code.");
        return;
      }
      fetch(`http://localhost:5000/api/v1/auth/verify/email`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        body: JSON.stringify({otp: verificationCode})
      }).then(async (res) => {
        if (!res.ok){
            alert('Invalid verification code');
            return;
        }
        setIsVerified(true);
        // wait for 2 seconds and redirect to the home
        setTimeout(() => {
            window.location.href = '/profile';
        }, 2000);
      })
    }


    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-sm text-center">
                <h1 className="text-2xl font-bold text-gray-800">Email Verification</h1>
                {isVerified ? (
                    <p className="mt-4 text-green-600 font-medium">Your email has been verified! ✅</p>
                ) : (
                    <div className="mt-4 space-y-4">
                        <input
                            type="text"
                            placeholder="Enter verification code"
                            value={verificationCode}
                            onChange={(e) => setVerificationCode(e.target.value)}
                            className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-400 outline-none"
                        />
                        <button
                            className="w-full bg-blue-600 text-white font-semibold p-2 rounded-lg hover:bg-blue-700 transition"
                            onClick={handleVerification}
                        >
                            Verify Email
                        </button>
                        {/* Resend Verification Token Button */}
                        <button
                            className={`text-blue-500 text-sm ${
                                isResendDisabled ? 'opacity-50 cursor-not-allowed' : ''
                            }`}
                            onClick={handleResendVerification}
                            disabled={isResendDisabled}
                        >
                            Resend verification token
                        </button>
                        {/* Countdown Timer */}
                        {isResendDisabled && (
                            <p className="text-gray-500 text-sm mt-2">You can resend in {countdown} seconds</p>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default VerifyEmailPage;
