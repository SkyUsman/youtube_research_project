// import useStatus from "@/hooks/useStatus";
import { Status } from "@/types/types";
import React from "react";

const Exit = ({
  setStatus,
}: {
  setStatus: React.Dispatch<React.SetStateAction<Status>>;
}) => {
  // Grab the status of the survey.
  // const { setStatus } = useStatus();

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
            All done! {":)"}
          </span>
        </div>
        <div>
          <span className="text-lg text-black font-normal">
            Thank you for participating in our survey, we really appreciate your
            insights and point of view.
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
            Be on the lookout for our results!
          </span>
        </div>
        <div className="flex flex-row justify-end items-center w-full">
          <button
            className="bg-black px-4 py-2 rounded-md text-white cursor-pointer hover:opacity-80 transition-all ease-in-out duration-300"
            onClick={() => setStatus("idle")}
          >
            <span className="text-sm text-inherit">Take Again</span>
          </button>
        </div>
      </div>
    </>
  );
};

export default Exit;
