"use client";
import React from "react";
import RadioButton from "../components/RadioButton";
import {
  CommentResponse,
  RadioOption,
  Status,
  SurveyResponse,
} from "@/types/types";
import { fetchComments, submitSurvey } from "@/services/api";
// import useStatus from "@/hooks/useStatus";
import Loader from "@/components/Loader";
import RadioProvider from "@/contexts/RadioContext";

const Question = ({
  setStatus,
}: {
  setStatus: React.Dispatch<React.SetStateAction<Status>>;
}) => {
  // Store the selected option.
  const [selectedOption, setSelectedOption] = React.useState<RadioOption>(null);

  // Store the current question.
  const [question, setQuestion] = React.useState<string | null>(null);
  const [index, setIndex] = React.useState<number>(0);

  // Store the results.
  const [results, setResults] = React.useState<SurveyResponse[]>([]);

  // Load the comments, loading, and error
  const [data, setData] = React.useState<CommentResponse[]>([]);
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const [isError, setIsError] = React.useState<boolean>(false);

  // Store the status and selected option.
  // const { setStatus } = useStatus();

  const loadComments = async () => {
    try {
      // Set the loading state.
      setIsLoading(true);

      // Fetch the comments.
      const res = await fetchComments();

      if (res && res.length > 0) {
        // Set the data
        setData(res);
        // Set the initial question immediately
        setQuestion(res[0].comment);
      }
    } catch (error) {
      console.error("Error loading comments:", error);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  };

  // Load the data only once on component mount.
  React.useEffect(() => {
    loadComments();
  }, []);

  // Handle the submission.
  const handleSubmission = async () => {
    try {
      // Guard against no data.
      if (!data) return;

      // Store the final result.
      const newRes = {
        id: data[index].id,
        response: selectedOption,
      };

      // Update the final results and post.
      const updatedRes = [...results, newRes];
      setResults(updatedRes);

      // Set submitting state to show loading spinner.
      setIsLoading(true);

      // Post the respoonses to the database.
      await submitSurvey(updatedRes);

      // Update the status.
      setStatus("done");
    } catch (error) {
      setIsLoading(false);
      setIsError(true);
      console.error("Error submitting the survey:", error);
    }
  };

  // Handle the previous click.
  const handlePreviousQuestion = () => {
    // Copy the results and remove the last entry.
    const updatedRes = [...results];
    const previous = updatedRes.pop();
    setResults(updatedRes);

    // Update the index.
    const newIdx = index - 1;
    setIndex(newIdx);

    // Update the question and previous response.
    if (data && data[newIdx]) {
      setQuestion(data[newIdx].comment);
      setSelectedOption(previous?.response ?? null);
    }
  };

  // Handle the next click.
  const handleNextQuestion = () => {
    // Guard for no data.
    if (!data) return;

    // Store the result.
    const newRes = {
      id: data[index].id,
      response: selectedOption,
    };

    // Reset selection for next question.
    setSelectedOption(null);

    // Append the results.
    const updatedRes = [...results, newRes];
    setResults(updatedRes);

    // Update the index.
    const newIdx = index + 1;
    setIndex(newIdx);

    // Update the question.
    setQuestion(data[newIdx].comment);
  };

  // Loading state.
  if (isLoading) return <Loader />;

  // Error State.
  if (isError || !data)
    return (
      <div className="text-center p-8 text-red-500">
        Error loading questions. Please try again by refreshing.
      </div>
    );

  return (
    <div className="w-full max-w-2xl mx-auto px-4 sm:px-6 md:px-8">
      <div className="flex items-center justify-center py-4">
        <span className="text-sm sm:text-base md:text-lg text-black opacity-50 font-normal">
          {`${index + 1} / ${data.length}`}
        </span>
      </div>
      <div className="flex flex-col gap-6">
        <div>
          <span className="text-lg sm:text-xl md:text-2xl text-black font-medium">
            Do you think the comment below could be classified as misinformation?
          </span>
        </div>
        <div className="bg-gray-100 p-4 rounded-md">
          <span className="text-base sm:text-lg md:text-xl text-black font-normal">
            <span className="text-black font-medium">Comment: </span>
            {`"${question}"`}
          </span>
        </div>
        <RadioProvider
          selectedOption={selectedOption}
          setSelectedOption={setSelectedOption}
        >
          <div className="flex flex-col gap-4">
            <RadioButton value="yes" label="Yes" />
            <RadioButton value="no" label="No" />
            <RadioButton value="skip" label="Skip" />
          </div>
        </RadioProvider>
      </div>
      <div className="flex flex-row justify-between items-center w-full py-4">
        {index > 0 && (
          <button
            className="bg-black px-5 py-3 rounded-md text-white cursor-pointer hover:opacity-80 transition-all ease-in-out duration-300"
            onClick={handlePreviousQuestion}
          >
            <span className="text-xs sm:text-sm md:text-base text-inherit">
              Previous
            </span>
          </button>
        )}
        <button
          className={`bg-black px-5 py-3 rounded-md text-white cursor-pointer hover:opacity-80 transition-all ease-in-out duration-300 ${
            !selectedOption ? "opacity-50 cursor-not-allowed" : "opacity-100"
          }`}
          onClick={
            index === data.length - 1 ? handleSubmission : handleNextQuestion
          }
          disabled={!selectedOption}
        >
          <span className="text-xs sm:text-sm md:text-base text-inherit">
            {index === data.length - 1 ? "Submit" : "Next"}
          </span>
        </button>
      </div>
    </div>
  );
};

export default Question;
