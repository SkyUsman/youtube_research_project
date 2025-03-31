import { Status } from "@/types/types";
import React from "react";

const Exit = ({
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
      <div className="flex flex-col gap-5 w-full sm:gap-6 md:gap-8">
        <div>
          <span className="text-lg sm:text-xl md:text-2xl text-black font-medium">
            All done! {":)"}
          </span>
        </div>
        <div>
          <span className="text-base sm:text-lg md:text-xl text-black font-normal">
            Thank you for participating in our survey, we really appreciate
            your insights and point of view.
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
            Be on the lookout for our results!
          </span>
        </div>
        <div className="flex flex-row justify-end items-center w-full">
          <button
            className="bg-black px-4 py-2 sm:px-5 sm:py-3 md:px-6 md:py-4 rounded-md text-white cursor-pointer hover:opacity-80 transition-all ease-in-out duration-300"
            onClick={() => setStatus("idle")}
          >
            <span className="text-xs sm:text-sm md:text-base text-inherit">
              Take Again
            </span>
          </button>
        </div>
      </div>
    </>
  );
};

export default Exit;
