import { RadioOption, Status } from "./types";

export interface RadioContextInterface {
  selectedOption: RadioOption | undefined;
  setSelectedOption: (option: RadioOption) => void | undefined;
}

export interface RadioProviderInterface {
  children: React.ReactNode;
  selectedOption: RadioOption | undefined;
  setSelectedOption: (option: RadioOption) => void | undefined;
}

export interface RadioOptionProps {
  value: RadioOption;
  label: string;
}

export interface StatusContextInterface {
  status: Status | undefined;
  setStatus: (option: Status) => void | undefined;
}

export interface StatusProviderInterface {
  children: React.ReactNode;
  status: Status | undefined;
  setStatus: (option: Status) => void | undefined;
}
