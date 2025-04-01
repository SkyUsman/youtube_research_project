import React from "react";
import {
  StatusContextInterface,
  StatusProviderInterface,
} from "@/types/interfaces";

// Create the context.
export const StatusContext = React.createContext<
  StatusContextInterface | undefined
>(undefined);

// Create the provider.
const StatusProvider: React.FC<StatusProviderInterface> = ({
  children,
  status,
  setStatus,
}) => {
  return (
    <StatusContext.Provider value={{ status, setStatus }}>
      {children}
    </StatusContext.Provider>
  );
};

export default StatusProvider;
