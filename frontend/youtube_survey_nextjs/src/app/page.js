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
} from "@mui/material"; // Import MUI components

export default function Home() {
  const [comments, setComments] = useState([]);
  const [responses, setResponses] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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

    // Calculate counts for yes, no, and skip
    const yesCount = Object.values(responses).filter(
      (response) => response === "yes"
    ).length;
    const noCount = Object.values(responses).filter(
      (response) => response === "no"
    ).length;
    const skipCount = Object.values(responses).filter(
      (response) => response === "maybe"
    ).length;

    // Prepare the data to send to the backend
    const responsePayload = {
      yes_count: yesCount,
      no_count: noCount,
      skip_count: skipCount,
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

      alert("Survey submitted successfully");
    } catch (error) {
      alert("Error submitting survey: " + error.message);
    }
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
      {" "}
      {/* OU Cream background */}
      <h1 className="text-5xl text-center mb-12 text-crimson font-bold">
        {" "}
        {/* OU Crimson title */}
        University of Oklahoma Disinformation Survey
      </h1>
      <Typography variant="body1" className="text-center mb-6">
        Please help us improve our understanding of disinformation by completing
        the survey below.
      </Typography>
      <form onSubmit={handleSubmit} className="space-y-8">
        {comments.map((comment, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-lg shadow-md space-y-4"
          >
            <Typography variant="body1" className="text-gray-600">
              Do you think this is disinformation?
            </Typography>

            <Typography variant="h6" className="text-crimson font-semibold">
              {comment}
            </Typography>

            <FormControl component="fieldset">
              <RadioGroup
                aria-label={`question-${index}`}
                name={`question-${index}`}
                onChange={(e) => handleResponseChange(index, e.target.value)}
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
    </div>
  );
}
