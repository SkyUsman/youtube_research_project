import RadioProvider from "@/contexts/RadioContext";
import { RadioGroupProps } from "@/types/interfaces";
import React from "react";

const RadioGroup: React.FC<RadioGroupProps> = ({
  children,
  value,
  onChange,
}) => {
  return (
    <RadioProvider value={value} onChange={onChange}>
      <div className="flex flex-col gap-5">{children}</div>
    </RadioProvider>
  );
};

export default RadioGroup;
