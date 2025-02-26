'use client';
import NavBar from "./ui/NavBar";
import WaveBackground from "./ui/WaveBg";
import {useState, useEffect} from 'react';
import InfoSection from "./InfoSection";

export default function Home() {
  const [isLogged, setIsLogged] = useState(false);
  return (
    <div className="h-screeen w-full flex flex-col justify-center items-center">
      {/* Making the toplevel navbar */}
      <NavBar isLogged={isLogged} />
      {/* Hero Section */}
      <div className="flex flex-col justify-center items-center w-fit px-10 gap-3 h-screen">
        <h1 className="text-6xl font-bold">Welcome to our <code className="bg-red-500 text-white rounded-md px-4">Ai Solution</code></h1>
        <p>This is some words that no one reads just used for decoration stuff and so on</p>
        <div className="flex gap-5 flex-row lg:flex-row">
          <button 
          className="bg-red-500 text-white p-3 rounded-full hover:bg-red-300"
          onClick={() => window.location.href = '/login'}
          >Get Started</button>
          <button className="bg-red-500 text-white p-3 rounded-full hover:bg-red-300">Learn more</button>
        </div>
      </div>
      {/* Info Section */}
      <InfoSection />
    </div>
  );
}
