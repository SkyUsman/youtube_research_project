"use client";
import React, { useState, useEffect } from "react";
import Question from "../components/Question";
import getComments from "@/api/getComments";
import postResponses from "@/api/postResponses";

export default function Home() {
  const [comments, setComments] = useState([
    { id: 1, text: "This is the first comment. Is this disinformation?" },
    { id: 2, text: "This is the second comment. Is this disinformation?" },
    { id: 3, text: "This is the third comment. Is this disinformation?" },
  ]);
  const [responses, setResponses] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch survey data from the API
  useEffect(() => {
    const fetchComments = async () => {
      try {
        const comments = await getComments(); // Call the getComments function
        setComments(comments);
        setLoading(false);
      } catch (err) {
        setError(err.message || "Failed to load comments");
        setLoading(false);
      }
    };

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
      await postResponses(responses); // Call the submitResponses function
      alert("Survey submitted successfully");
    } catch (error) {
      alert("Error submitting survey: " + error.message);
    }
  };

  if (loading) return <p>Loading...</p>;
  // if (error) return <p>{error}</p>;

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-4xl text-center mb-8">Survey</h1>
      <form onSubmit={handleSubmit}>
        {comments.map((comment) => (
          <Question
            key={comment.id}
            question={comment}
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
