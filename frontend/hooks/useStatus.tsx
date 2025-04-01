import { StatusContext } from "@/contexts/StatusContext";
import { StatusContextInterface } from "@/types/interfaces";
import React from "react";

const useStatus = () => {
  // Create an instance of the context.
  const context = React.useContext<StatusContextInterface | undefined>(
    StatusContext
  );

  // Guard against any error.
  if (context === undefined) {
    throw new Error("useStatus hook must be used within the StatusProvider");
  }

  // Return the context.
  return context;
};

export default useStatus;
