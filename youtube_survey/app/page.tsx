"use client";
import Image from "next/image";
import Initial from "@/pages/Initial";
import Question from "@/pages/Question";
import Exit from "@/pages/Exit";
import React from "react";
import { Status } from "@/types/types";
import StatusGroup from "@/components/StatusGroup";

// When next button on inital is clicked, loading should appear until data is returned (useSWR built in loading).
// Once data is returned, needs to be used within question object. Once user hits next, needs to be stored in a stack to hold responses. Once we make it to the end, post the responses.
// Things to note: techinally, all the data (10 comments) will be loaded in at once, but we only need to display one, until the user clicks the next button, which will populate a sepearte question compoenent.

const Home = () => {
  // Track the progress of the survey.
  const [status, setStatus] = React.useState<Status>("idle");

  return (
    <div className="flex justify-center items-center h-screen w-full bg-crimson">
      <div className="flex flex-col justify-center items-center p-8 gap-5 bg-white rounded-xl w-1/3 h-fit shadow-md">
        <StatusGroup value={status} onChange={setStatus}>
          {status === "idle" && <Initial />}
          {status === "started" && <Question />}
          {status === "done" && <Exit />}
        </StatusGroup>
      </div>
    </div>
  );
};

export default Home;
