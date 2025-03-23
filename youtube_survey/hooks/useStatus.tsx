import { StatusContext } from "@/contexts/StatusContext";
import React from "react";

const useStatus = () => {
  // Create an instance of the context.
  const context = React.useContext(StatusContext);

  // Guard against any error.
  if (context === undefined)
    throw new Error("useRadio hook must be used within the RadioProvider");

  // Return the context.
  return context;
};

export default useStatus;
