import { RadioContext } from "@/contexts/RadioContext";
import { RadioContextInterface } from "@/types/interfaces";
import React from "react";

const useRadio = () => {
  // Create an instance of the context.
  const context = React.useContext<RadioContextInterface | undefined>(
    RadioContext
  );

  // Guard against any error.
  if (context === undefined)
    throw new Error("useRadio hook must be used within the RadioProvider");

  // Return the context.
  return context;
};

export default useRadio;
