import React from "react";
import { motion } from "framer-motion";

const wavePaths = new Array(10).fill("").map((_, index) => ({
  delay: [0, 2.5, 6, 4, 1, 5, 3, 1.5, 5.5, 1][index], // Animation delays
  translateY: index * 100, // Different Y positions
}));

const WaveBackground = () => {
  return (
    <div className="absolute flex w-screen overflow-hidden justify-center items-center bg-black">
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 1500 1000"
        xmlns="http://www.w3.org/2000/svg"
        className="rotate-[-45deg]"
      >
        <g stroke="none" strokeWidth="1" fill="none" fillRule="evenodd" strokeLinecap="round">
          {wavePaths.map((wave, index) => (
            <motion.path
              key={index}
              d="M16,16 C76.235,16 77.932,77 138.167,77 C198.402,77 198.402,16 260.333,16 
                C320.568,16 322.265,77 382.5,77 C442.735,77 442.735,16 504.667,16 
                C564.902,16 566.598,77 626.833,77 C687.068,77 687.068,16 749,16 
                C809.235,16 810.932,77 871.167,77 C931.402,77 931.402,16 993.333,16 
                C1053.568,16 1055.265,77 1115.5,77 C1175.735,77 1175.735,16 1237.667,16 
                C1297.902,16 1299.598,77 1359.833,77 C1420.068,77 1420.068,16 1482,16"
              strokeWidth="32"
              stroke="#FBC02E"
              initial={{ strokeDasharray: 700, strokeDashoffset: 10, y: wave.translateY }}
              animate={{
                strokeDashoffset: 9800,
                stroke: ["#FBC02E", "#19D8FF", "#FBC02E"],
                transition: {
                  duration: 15,
                  repeat: Infinity,
                  ease: "linear",
                  delay: wave.delay,
                },
              }}
            />
          ))}
        </g>
      </svg>
    </div>
  );
};

export default WaveBackground;
