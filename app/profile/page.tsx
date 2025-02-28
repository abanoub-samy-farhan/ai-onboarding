'use client'
import React, { useState, useEffect } from 'react';

// Simulating API response (Replace with actual API call)
const mockUserData = {
    id: 1,
    full_name: 'John Doe',
    email: 'johndoe@example.com',
    national_id: '123456789',
    address: '123 Main St, New York, NY',
    phone_number: '+1 234 567 890',
    identity_verified: false,
    email_verified: false,
    is_active: false
};

const ProfilePage: React.FC = () => {
    const [user, setUser] = useState(mockUserData);

    useEffect(() => {
        fetch('http://localhost:5000/api/v1/user/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        }).then(async (res) => {
            if (!res.ok){
                console.log(await res.json());
            }
            const data = await res.json();
            setUser(data);
            console.log(data);
        })
    }
    , []);

    // Define Onboarding Steps
    const onboardingSteps = [
        { id: 1, text: 'Verify Email', completed: user.email_verified },
        { id: 2, text: 'Verify Identity', completed: user.identity_verified },
        {
            id: 3,
            text: 'Upload Documents',
            completed: false,
            locked: !user.email_verified || !user.identity_verified
        }
    ];

    // Function to complete a step (Mock Update)
    const completeStep = (id: number) => {
        if (id === 1) setUser(prev => ({ ...prev, email_verified: true }));
        if (id === 2) setUser(prev => ({ ...prev, identity_verified: true }));
    };


    const handleSendVerification = async () => {
        fetch('http://localhost:5000/api/v1/auth/generate/otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        }).then(async (res) => {
            if (!res.ok){
                console.log(await res.json());
            }
        }).catch((err) => {
            console.error(err);
        })          
        }

    // Update Account Activation Status
    useEffect(() => {
        if (user.email_verified && user.identity_verified) {
            setUser(prev => ({ ...prev, is_active: true }));
        }
    }, [user.email_verified, user.identity_verified]);

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
                {/* User Info */}
                <div className="flex items-center space-x-4">
                    <img
                        src="https://i.pravatar.cc/100"
                        alt="User"
                        className="w-16 h-16 rounded-full border border-gray-300"
                    />
                    <div>
                        <h1 className="text-2xl font-bold text-gray-800">{user.full_name}</h1>
                        <p className={`mt-1 text-lg font-semibold ${user.is_active ? 'text-green-600' : 'text-red-500'}`}>
                            {user.is_active ? '✅ Account Active' : '❌ Account Inactive'}
                        </p>
                    </div>
                </div>

                {/* User Details */}
                <div className="mt-4 text-gray-700 text-sm">
                    <p><strong>Email:</strong> {user.email}</p>
                    <p><strong>Phone:</strong> {user.phone_number}</p>
                    <p><strong>Address:</strong> {user.address}</p>
                    <p><strong>National ID:</strong> {user.national_id}</p>
                </div>

                {/* Onboarding Steps */}
                <div className="mt-6">
                    <h2 className="text-lg font-semibold text-gray-700">Onboarding Steps</h2>
                    <ul className="mt-3 space-y-3">
                        {onboardingSteps.map(step => (
                            <li
                                key={step.id}
                                className={`p-3 flex justify-between items-center border rounded-lg ${
                                    step.completed ? 'bg-green-100 border-green-500' : 'bg-gray-50 border-gray-300'
                                }`}
                            >
                                <span className={step.completed ? 'text-green-600' : 'text-gray-800'}>
                                    {step.text}
                                </span>
                                {!step.completed && !step.locked && (
                                    <button
                                        onClick={async () => {
                                            if (step.id === 1){
                                                await handleSendVerification();
                                                window.location.href = '/profile/verify-email';
                                            }
                                            else if (step.id === 2){
                                                window.location.href = '/profile/verify-identity';
                                            }
                                            else if (step.id === 3){
                                                window.location.href = '/profile/upload-documents';
                                            }
                                        }}
                                        className="px-3 py-1 text-sm font-semibold text-white bg-blue-500 rounded-lg hover:bg-blue-600"
                                    >
                                        Complete
                                    </button>
                                )}
                                {step.locked && <span className="text-gray-500 text-sm">🔒 Locked</span>}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;
