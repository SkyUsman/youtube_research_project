import { RadioOption, Status } from "./types";

export interface RadioContextInterface {
  selectedOption: RadioOption | undefined;
  setSelectedOption: (option: RadioOption) => void | undefined;
}

export interface RadioProviderInterface {
  children: React.ReactNode;
  value: RadioOption;
  onChange: (value: RadioOption) => void;
}

export interface RadioGroupProps {
  children: React.ReactNode;
  value: RadioOption;
  onChange: (value: RadioOption) => void;
}

export interface RadioOptionProps {
  value: RadioOption;
  label: string;
}

export interface StatusContextInterface {
  status: Status;
  setStatus: (option: Status) => void;
}

export interface StatusProviderInterface {
  children: React.ReactNode;
  initialValue?: Status;
  onChange?: (value: Status) => void;
}

export interface StatusGroupProps {
  children: React.ReactNode;
  value: Status;
  onChange: (value: Status) => void;
}
