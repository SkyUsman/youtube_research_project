"use client";
import { Status } from "@/types/types";
import React from "react";
import Initial from "./Initial";
import Question from "./Question";
import Exit from "./Exit";

const Content = () => {
  // Store the status state.
  const [status, setStatus] = React.useState<Status>("idle");

  return (
    <>
      {status === "idle" && <Initial setStatus={setStatus} />}
      {status === "started" && <Question setStatus={setStatus} />}
      {status === "done" && <Exit setStatus={setStatus} />}
    </>
  );
};

export default Content;
