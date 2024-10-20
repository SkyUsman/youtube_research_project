"use client";
import React, { useState, useEffect } from "react";
import Question from "../components/Question";

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
  // useEffect(() => {
  //   // Fetch comments from your API
  //   const fetchComments = async () => {
  //     try {
  //       const res = await fetch("/api/getComments");
  //       const data = await res.json();

  //       if (res.ok) {
  //         setComments(data);
  //         setLoading(false);
  //       } else {
  //         setError(data.message);
  //       }
  //     } catch (err) {
  //       setError("Failed to load comments");
  //     }
  //   };

  //   fetchComments();
  // }, []);

  // Handle answer change
  const handleResponseChange = (id, value) => {
    setResponses((prev) => ({
      ...prev,
      [id]: value,
    }));
  };

  const handleSubmit = async (e) => {
    // e.preventDefault();

    // // Send responses to backend
    // try {
    //   const res = await fetch("/api/submitResponses", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify(responses),
    //   });

    //   if (res.ok) {
    //     alert("Survey submitted successfully");
    //   } else {
    //     alert("Failed to submit survey");
    //   }
    // } catch (error) {
    //   alert("Error submitting survey");
    // }
    return "Helo";
  };

  // if (submitted) {
  //   return (
  //     <h1 className="text-center text-2xl mt-8">
  //       Thank you for submitting your responses!
  //     </h1>
  //   );
  // }

  // if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

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
