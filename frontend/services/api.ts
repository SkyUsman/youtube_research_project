import { CommentResponse, SurveyResponse } from "@/types/types";

// Load in the API URL.
// const apiURL = process.env.NEXT_PUBLIC_API_URL;
const apiURL = "http://127.0.0.1:5000";

/**
 * Fetch the 10 random comments.
 * @returns
 */
export const fetchComments = async (): Promise<CommentResponse[]> => {
  const response = await fetch(`${apiURL}/comments/filtered/random`);
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
    const res = await fetch(`${apiURL}/comments/responses`, {
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
