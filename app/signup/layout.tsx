'use client'
import React from 'react';

const LoginLayout: React.FC = ({ children }) => {
    return (
        <div style={styles.container}>
            <div style={styles.formContainer}>
                {children}
            </div>
        </div>
    );
};

const styles: { [key: string]: React.CSSProperties } = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#f0f2f5',
    },
    formContainer: {
        width: '100%',
        height: 'fit-content',
        maxWidth: '500px',
        padding: '20px',
        backgroundColor: '#fff',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        borderRadius: '8px',
    },
};

export default LoginLayout;