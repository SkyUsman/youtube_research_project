"use client";
import React, { useState, useEffect } from "react";
import {
  Button,
  CircularProgress,
  RadioGroup,
  FormControlLabel,
  Radio,
  Typography,
  FormControl,
  Card,
  CardContent,
} from "@mui/material"; // Import MUI components

export default function Home() {
  const [comments, setComments] = useState([]);
  const [responses, setResponses] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false); // New state for submission status

  const fetchComments = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/getComments"); // Fetch comments from the API
      if (!response.ok) {
        throw new Error("Failed to load comments");
      }
      const data = await response.json(); // Extract JSON data
      setComments(data); // Set comments state
      setLoading(false);
    } catch (err) {
      setError(err.message || "Failed to load comments");
      console.error(err);
      setLoading(false);
    }
  };

  // Fetch survey data from the API
  useEffect(() => {
    fetchComments();
  }, []);

  // Handle answer change
  const handleResponseChange = (id, value) => {
    setResponses((prev) => ({
      ...prev,
      [id]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Prepare the response data to include comment_id and the respective answer
    const responsePayload = {
      responses: comments.map((comment) => ({
        comment_id: comment.comment_id,
        yes_count: responses[comment.comment_id] === "yes" ? 1 : 0,
        no_count: responses[comment.comment_id] === "no" ? 1 : 0,
        skip_count: responses[comment.comment_id] === "maybe" ? 1 : 0,
      })),
    };

    // Send responses to backend via fetch
    try {
      const postResponse = await fetch(
        "http://127.0.0.1:5000/api/postResponses",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(responsePayload), // Convert the payload to JSON
        }
      );

      if (!postResponse.ok) {
        throw new Error("Error submitting survey");
      }

      setSubmitted(true); // Update the submitted state
      setResponses({}); // Reset responses after submission
    } catch (error) {
      alert("Error submitting survey: " + error.message);
    }
  };

  const handleNewSurvey = () => {
    setSubmitted(false); // Reset submission status to show the survey again
    setResponses({}); // Clear responses
    fetchComments(); // Optionally, re-fetch comments if needed
  };

  if (loading)
    return (
      <div className="flex justify-center items-center h-screen">
        <CircularProgress color="primary" /> {/* Material UI loading spinner */}
      </div>
    );

  if (error) return <p>{error}</p>; // Display error if there is one

  return (
    <div className="mx-auto p-8 bg-cream min-h-screen">
      {/* OU Cream background */}
      <h1 className="text-5xl text-center mb-12 text-crimson font-bold">
        University of Oklahoma Disinformation Survey
      </h1>
      <Typography variant="body1" className="text-center mb-6">
        Please help us improve our understanding of disinformation by completing
        the survey below.
      </Typography>

      {submitted ? (
        // Render the thank you card after submission
        <Card variant="outlined" className="mx-auto w-1/2 p-4">
          <CardContent>
            <Typography variant="h5" className="text-center mb-2">
              Thank you for submitting!
            </Typography>
            <Typography variant="body1" className="text-center mb-4">
              Your responses have been recorded.
            </Typography>
            <div className="text-center">
              <Button
                variant="contained"
                className="bg-crimson hover:bg-red-700 text-white"
                onClick={handleNewSurvey}
              >
                Submit a New Survey
              </Button>
            </div>
          </CardContent>
        </Card>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-8">
          {comments.map((comment) => (
            <div
              key={comment.comment_id}
              className="bg-white p-6 rounded-lg shadow-md space-y-4"
            >
              <Typography variant="body1" className="text-gray-600">
                Do you think this is disinformation?
              </Typography>

              <Typography variant="h6" className="text-crimson font-semibold">
                {comment.comment}
              </Typography>

              <FormControl component="fieldset">
                <RadioGroup
                  aria-label={`question-${comment.comment_id}`}
                  name={`question-${comment.comment_id}`}
                  onChange={(e) =>
                    handleResponseChange(comment.comment_id, e.target.value)
                  }
                  className="space-y-2"
                >
                  <FormControlLabel
                    value="yes"
                    control={<Radio color="primary" />}
                    label="Yes"
                  />
                  <FormControlLabel
                    value="no"
                    control={<Radio color="primary" />}
                    label="No"
                  />
                  <FormControlLabel
                    value="maybe"
                    control={<Radio color="primary" />}
                    label="Maybe"
                  />
                </RadioGroup>
              </FormControl>
            </div>
          ))}

          <div className="text-center mt-12">
            <Button
              type="submit"
              variant="contained"
              className="bg-crimson hover:bg-red-700 text-white py-2 px-6 rounded"
              style={{ fontSize: "1.1rem" }}
            >
              Submit
            </Button>
          </div>
        </form>
      )}
    </div>
  );
}
