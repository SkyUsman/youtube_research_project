"use client";
import React, { useState, useEffect } from "react";
import Question from "../components/Question";
import postResponses from "@/api/postResponses";

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

    // Send responses to backend
    try {
      await postResponses(responses); // Call the postResponses function
      alert("Survey submitted successfully");
    } catch (error) {
      alert("Error submitting survey: " + error.message);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>; // Display error if there is one

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-4xl text-center mb-8">Disinformation Survey</h1>
      <form onSubmit={handleSubmit}>
        {comments.map((comment, index) => (
          <Question
            key={index} // Use index as key, but consider using a unique ID if available
            question={{ text: comment }} // Pass comment text as the question prop
            onChange={handleResponseChange}
          />
        ))}
        <div className="text-center mt-8">
          <button
            type="submit"
            className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
}
