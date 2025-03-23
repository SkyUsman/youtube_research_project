import useStatus from "@/hooks/useStatus";
import React from "react";

const Initial = () => {
  // Grab the status of the survey.
  const { setStatus } = useStatus();

  return (
    <>
      <div className="flex items-center justify-center p-3 w-full">
        <span className="text-base text-black opacity-50 font-normal">
          YouTube Misinformation: Research at the University of Oklahoma
        </span>
      </div>
      <div className="flex flex-col gap-5 w-full">
        <div>
          <span className="text-xl text-black font-medium">
            Hey, please join us in understanding how disinformation spreads and
            affects online platforms!
          </span>
        </div>
        <div>
          <span className="text-lg text-black font-normal">
            Your insights are valued tremendously as we aim to pin point a main
            source of truth.
          </span>
        </div>
        <div>
          <span className="text-lg text-black font-normal">
            All submissions are entirely anonymous. Source code is avaliable as
            proof, if requested.
          </span>
        </div>
        <div>
          <span className="text-lg text-black font-normal">
            Structure: you will be provided 10 comments, of which you will
            classify as ‘yes’, ‘no’, or ‘skip’. That is all!
          </span>
        </div>
      </div>
      <div className="flex flex-row justify-end items-center w-full">
        <button
          className="bg-black px-4 py-2 rounded-md text-white cursor-pointer hover:opacity-80 transition-all ease-in-out duration-300"
          onClick={() => setStatus("started")}
        >
          <span className="text-sm text-inherit">Next</span>
        </button>
      </div>
    </>
  );
};

export default Initial;
