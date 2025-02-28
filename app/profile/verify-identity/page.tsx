'use client'
import React, { useState, useRef } from 'react';

const IdentityVerification: React.FC = () => {
    const [idFile, setIdFile] = useState<File | null>(null);
    const [videoBlob, setVideoBlob] = useState<Blob | null>(null);
    const [isRecording, setIsRecording] = useState(false);
    const [countdown, setCountdown] = useState(10);
    const videoRef = useRef<HTMLVideoElement>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const streamRef = useRef<MediaStream | null>(null);
    const recordedChunksRef = useRef<Blob[]>([]);

    // Handle File Upload
    const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            setIdFile(event.target.files[0]);
        }
    };

    // Start Recording Video
    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            streamRef.current = stream;
            if (videoRef.current) videoRef.current.srcObject = stream;

            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;
            recordedChunksRef.current = [];

            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    recordedChunksRef.current.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const recordedBlob = new Blob(recordedChunksRef.current, { type: 'video/webm' });
                setVideoBlob(recordedBlob);
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorder.start();
            setIsRecording(true);
            setCountdown(10);

            // Start countdown
            const countdownInterval = setInterval(() => {
                setCountdown(prev => {
                    if (prev <= 1) {
                        clearInterval(countdownInterval);
                        mediaRecorder.stop();
                        setIsRecording(false);
                    }
                    return prev - 1;
                });
            }, 1000);
        } catch (error) {
            console.error('Error accessing camera:', error);
            alert('Could not access the camera. Please allow camera permissions.');
        }
    };

    const handleVerifyIdentity = (idFile: File, videoBlob: Blob) => {
        const formData = new FormData();
        formData.append('identity_card_photo', idFile);
        formData.append('identity_card_video', videoBlob);
        fetch('http://localhost:5000/api/v1/auth/verify/identity', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            },
            body: formData
        }).then(async res => {
            if (!res.ok) {
                console.error(await res.json());
                alert('Identity verification failed. Please try again.');
            } else {
                alert('Identity verified successfully!');
                window.location.href = '/profile';
            }
        })
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
            <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
                <h1 className="text-2xl font-bold text-gray-800 text-center">Identity Verification</h1>

                {/* Step 1: Upload National ID */}
                <div className="mt-4">
                    <label className="block font-semibold text-gray-700">Upload National ID (PDF, JPG, JPEG, PNG)</label>
                    <input
                        type="file"
                        accept=".jpg, .jpeg, .png"
                        onChange={handleFileUpload}
                        className="mt-2 w-full border p-2 rounded-lg"
                    />
                    {idFile && (
                        <p className="mt-2 text-green-600 font-medium">
                            ✅ File Uploaded: {idFile.name}
                        </p>
                    )}
                </div>

                {/* Step 2: Record Video */}
                <div className="mt-6">
                    <h2 className="font-semibold text-gray-700">Record a 10-second Video</h2>
                    <video ref={videoRef} className="w-full mt-2 bg-black rounded-md" autoPlay muted />
                    {isRecording ? (
                        <p className="mt-2 text-red-500 font-semibold">Recording... {countdown}s left</p>
                    ) : (
                        <button
                            onClick={startRecording}
                            className="mt-2 w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition"
                        >
                            Start Recording
                        </button>
                    )}
                </div>

                {/* Step 3: Preview Video & Verify Identity */}
                {videoBlob && (
                    <div className="mt-6">
                        <h2 className="font-semibold text-gray-700">Preview Recorded Video</h2>
                        <video src={URL.createObjectURL(videoBlob)} controls className="w-full mt-2 rounded-md" />
                        <button
                            onClick={() => handleVerifyIdentity(idFile, videoBlob)}
                            className="mt-4 w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
                        >
                            Verify Identity
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default IdentityVerification;
