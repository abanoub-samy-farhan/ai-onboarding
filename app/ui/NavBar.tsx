import React from 'react';

export default function NavBar({ isLogged = false }) {
    return (
        <nav className="flex justify-around items-center flex-row fixed top-2 bg-gray-800 
            text-white border-b-2 rounded-2xl hover:shadow-lg
            transition-all duration-500 ease-in-out
            md:w-1/4 md:hover:w-1/3"
        >
            <ul className="flex items-center flex-row gap-5 p-5">
                <li>Home</li>
                <li>About</li>
                <li>Contact</li>
            </ul>
            {/* Divider */}
            <span className="w-0.5 h-10 bg-white"></span>
            {/* Profile or Get Started */}
            <div className="flex items-center gap-5 p-5">
                {isLogged ? <div>Profile</div> : <div>Get Started</div>}
            </div>
        </nav>
    );
}
