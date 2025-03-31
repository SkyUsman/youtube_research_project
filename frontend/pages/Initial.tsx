"use client";
// import useStatus from "@/hooks/useStatus";
import { Status } from "@/types/types";
import React from "react";

const Initial = ({
  setStatus,
}: {
  setStatus: React.Dispatch<React.SetStateAction<Status>>;
}) => {
  return (
    <>
      <div className="flex items-center justify-center p-3 w-full sm:p-4 md:p-5 lg:p-6">
        <span className="text-sm sm:text-base md:text-lg text-black opacity-50 font-normal text-center">
          YouTube Misinformation: Research at the University of Oklahoma
        </span>
      </div>
      <div className="flex flex-col gap-5 sm:gap-6 md:gap-8 w-full">
        <div>
          <span className="text-lg sm:text-xl md:text-2xl text-black font-medium">
            Hey, please join us in understanding how disinformation spreads and
            affects online platforms!
          </span>
        </div>
        <div>
          <span className="text-base sm:text-lg md:text-xl text-black font-normal">
            Your insights are valued tremendously as we aim to pinpoint a main
            source of truth.
          </span>
        </div>
        <div>
          <span className="text-base sm:text-lg md:text-xl text-black font-normal">
            All submissions are entirely anonymous. Source code is available as
            proof, if requested.
          </span>
        </div>
        <div>
          <span className="text-base sm:text-lg md:text-xl text-black font-normal">
            Structure: you will be provided 10 comments, of which you will
            classify as ‘yes’, ‘no’, or ‘skip’. That is all!
          </span>
        </div>
      </div>
      <div className="flex flex-row justify-end items-center w-full">
        <button
          className="bg-black px-4 py-2 sm:px-5 sm:py-3 md:px-6 md:py-4 rounded-md text-white cursor-pointer hover:opacity-80 transition-all ease-in-out duration-300"
          onClick={() => setStatus("started")}
        >
          <span className="text-xs sm:text-sm md:text-base text-inherit">
            Next
          </span>
        </button>
      </div>
    </>
  );
};

export default Initial;
