"use client";
import useRadio from "@/hooks/useRadio";
import { RadioOptionProps } from "@/types/interfaces";
import React from "react";

const RadioButton: React.FC<RadioOptionProps> = ({ value, label }) => {
  // Extract the selected option from the context.
  const { selectedOption, setSelectedOption } = useRadio();

  return (
    <div
      className={`flex flex-row items-center p-3 rounded-md border cursor-pointer group border-gray-300 
                  sm:p-4 md:p-5 lg:p-6`}
      onClick={() => setSelectedOption(value)}
    >
      <div
        className={`w-5 h-5 rounded-full border mr-3 flex items-center justify-center sm:w-6 sm:h-6 md:w-7 md:h-7 lg:w-8 lg:h-8 
              ${
                selectedOption !== value && "group-hover:border-black"}`
              }
      >
        <div
          className={`w-3 h-3 rounded-full sm:w-4 sm:h-4 md:w-5 md:h-5 lg:w-6 lg:h-6 
              ${
                selectedOption === value ? "bg-black" : "bg-transparent"
              } transition-all ease-in-out duration-200`}
        />
      </div>
      <span className="text-base sm:text-lg md:text-xl lg:text-2xl">{label}</span>
    </div>
  );
};

export default RadioButton;
