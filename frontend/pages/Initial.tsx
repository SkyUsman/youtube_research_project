"use client";
import { Status } from "@/types/types";
import React from "react";

const Initial = ({
  setStatus,
}: {
  setStatus: React.Dispatch<React.SetStateAction<Status>>;
}) => {
  return (
    <>
      <div className="flex items-center justify-center p-3 w-full">
        <span className="2xl:text-base xl:text-sm lg:text-base sm:text-sm text-xs text-black opacity-50 font-normal">
          YouTube Misinformation: Research at the University of Oklahoma
        </span>
      </div>
      <div className="flex flex-col gap-5 w-full">
        <div>
          <span className="2xl:text-xl xl:text-lg lg:text-xl md:text-lg sm:text-base text-base text-black font-medium">
            Hey, please join us in understanding how disinformation spreads and
            affects online platforms!
          </span>
        </div>
        <div>
          <span className="2xl:text-lg xl:text-base lg:text-lg md:text-base sm:text-sm text-sm text-black font-normal">
            Your insights are valued tremendously as we aim to pin point a main
            source of truth.
          </span>
        </div>
        <div>
          <span className="2xl:text-lg xl:text-base lg:text-lg md:text-base sm:text-sm text-sm text-black font-normal">
            All submissions are entirely anonymous. Source code is avaliable as
            proof, if requested.
          </span>
        </div>
        <div>
          <span className="2xl:text-lg xl:text-base lg:text-lg md:text-base sm:text-sm text-sm text-black font-normal">
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
