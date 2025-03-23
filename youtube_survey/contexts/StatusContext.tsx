"use client";
import React from "react";
import {
  StatusContextInterface,
  StatusProviderInterface,
} from "@/types/interfaces";
import { Status } from "@/types/types";

// Create the context.
export const StatusContext = React.createContext<
  StatusContextInterface | undefined
>(undefined);

// Create the provider.
const StatusProvider: React.FC<StatusProviderInterface> = ({
  children,
  initialValue = "idle",
  onChange,
}) => {
  // Store the state.
  const [status, setStatus] = React.useState<Status>(initialValue);

  // Handle the option change.
  const handleStatusChange = (option: Status) => {
    // Set the option.
    setStatus(option);

    //Do more, if specified.
    if (onChange) onChange(option);
  };

  return (
    <StatusContext.Provider value={{ status, setStatus: handleStatusChange }}>
      {children}
    </StatusContext.Provider>
  );
};

export default StatusProvider;
