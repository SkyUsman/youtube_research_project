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
                  sm:p-4`}
      onClick={() => setSelectedOption(value)}
    >
      <div
        className={`w-5 h-5 rounded-full border mr-3 flex items-center justify-center 
              ${selectedOption !== value && "group-hover:border-black"}`}
      >
        <div
          className={`w-3 h-3 rounded-full
              ${
                selectedOption === value ? "bg-black" : "bg-transparent"
              } transition-all ease-in-out duration-200`}
        />
      </div>
      <span className="sm:text-base text-sm">{label}</span>
    </div>
  );
};

export default RadioButton;
