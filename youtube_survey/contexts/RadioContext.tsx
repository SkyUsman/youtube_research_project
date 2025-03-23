"use client";
import React from "react";
import {
  RadioContextInterface,
  RadioProviderInterface,
} from "@/types/interfaces";

// Create the context.
export const RadioContext = React.createContext<
  RadioContextInterface | undefined
>(undefined);

// Create the provider.
const RadioProvider: React.FC<RadioProviderInterface> = ({
  children,
  value,
  onChange,
}) => {
  return (
    <RadioContext.Provider
      value={{ selectedOption: value, setSelectedOption: onChange }}
    >
      {children}
    </RadioContext.Provider>
  );
};

export default RadioProvider;
