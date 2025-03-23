import { CommentResponse, SurveyResponse } from "@/types/types";

/**
 * Fetch the 10 random comments.
 * @returns
 */
export const fetchComments = async (): Promise<CommentResponse[]> => {
  const response = await fetch(
    "http://127.0.0.1:5000/comments/filtered/random"
  );
  if (!response.ok) {
    throw new Error(`Failed to fetch comments, status code ${response.status}`);
  }
  return response.json();
};

/**
 * Submit all responses to the server
 * @param responses - Array of user responses
 * @returns Promise that resolves to the server response
 */
export const submitSurvey = async (responses: SurveyResponse[]) => {
  try {
    // Post to the API.
    const res = await fetch("http://127.0.0.1:5000/comments/responses", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ responses }),
    });

    // Guard against any errors.
    if (!res.ok)
      throw new Error(`Failed to submit responses, status code ${res.status}`);
    console.log(res);
    // return await res.json();
  } catch (error) {
    console.error("Error submitting responses:", error);
    throw error;
  }
};

// Define your fetcher function
// const fetcher = async (url: string): Promise<CommentResponse[]> => {
//   const response = await fetch(url);
//   if (!response.ok) {
//     throw new Error(`Failed to fetch comments, status code ${response.status}`);
//   }
//   return response.json();
// };

/**
 * Hook to fetch comments data
 * @returns {Object} - Object with comments data, loading, and error states
 */
// export const useComments = () => {
//   // Fetch the data from the API, using useSWR's built in fetch.
//   const { data, error, isLoading } = useSWR<CommentResponse[]>(
//     "http://127.0.0.1:5000/comments/filtered/random",
//     null
//   );

//   return {
//     data,
//     isError: error,
//     isLoading,
//   };
// };
