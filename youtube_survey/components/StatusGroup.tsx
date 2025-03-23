import StatusProvider from "@/contexts/StatusContext";
import { StatusGroupProps } from "@/types/interfaces";
import React from "react";

const StatusGroup: React.FC<StatusGroupProps> = ({
  children,
  value,
  onChange,
}) => {
  return (
    <StatusProvider initialValue={value} onChange={onChange}>
      {children}
    </StatusProvider>
  );
};

export default StatusGroup;
