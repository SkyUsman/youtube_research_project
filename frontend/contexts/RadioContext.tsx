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
  selectedOption,
  setSelectedOption,
}) => {
  return (
    <RadioContext.Provider value={{ selectedOption, setSelectedOption }}>
      {children}
    </RadioContext.Provider>
  );
};

export default RadioProvider;
