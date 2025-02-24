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
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@mui/material";

export default function Home() {
  const [comments, setComments] = useState([]);
  const [responses, setResponses] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [errorModal, setErrorModal] = useState(false); // State for error modal

  const fetchComments = async () => {
    try {
      const response = await fetch(
        "https://ytresearchflask.online/api/getComments"
      );
      if (!response.ok) {
        throw new Error(
          "Failed to load comments and generate survey. Please refresh the page!"
        );
      }
      const data = await response.json();
      setComments(data);
      setLoading(false);
    } catch (err) {
      setError(
        err.message ||
          "Failed to load comments and generate survey. Please refresh the page!"
      );
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComments();
  }, []);

  const handleResponseChange = (id, value) => {
    setResponses((prev) => ({
      ...prev,
      [id]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // const unansweredQuestions = comments.some(
    //   (comment) => !responses[comment.comment_id]
    // );

    // if (unansweredQuestions) {
    //   setErrorModal(true);
    //   return;
    // }

    const responsePayload = {
      responses: comments.map((comment) => ({
        comment_id: comment.comment_id,
        yes_count: responses[comment.comment_id] === "yes" ? 1 : 0,
        no_count: responses[comment.comment_id] === "no" ? 1 : 0,
        skip_count: responses[comment.comment_id] === "maybe" ? 1 : 0,
      })),
    };

    try {
      const postResponse = await fetch(
        "https://ytresearchflask.online/api/postResponses",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(responsePayload),
        }
      );

      if (!postResponse.ok) {
        throw new Error("Error submitting survey");
      }

      setSubmitted(true);
      setResponses({});
    } catch (error) {
      alert("Error submitting survey: " + error.message);
    }
  };

  const handleNewSurvey = () => {
    setSubmitted(false);
    setResponses({});
    fetchComments();
  };

  const closeErrorModal = () => {
    setErrorModal(false);
  };

  if (loading)
    return (
      <div className="flex justify-center items-center h-screen">
        <CircularProgress color="primary" />
      </div>
    );

  if (error) return <p>{error}</p>;

  return (
    <div className="mx-auto p-8 bg-cream min-h-screen">
      <h1 className="text-5xl text-center mb-12 text-crimson font-bold">
        Exploring Disinformation: A University of Oklahoma Study
      </h1>
      <Typography variant="body1" className="text-center mb-6 text-black">
        Join us in understanding how disinformation spreads and affects online
        platforms. Your insights will contribute to research aimed at
        identifying and addressing misleading information on YouTube. Please
        take a few moments to complete the survey below.
      </Typography>

      {submitted ? (
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
                    color="black"
                  />
                  <FormControlLabel
                    value="no"
                    control={<Radio color="primary" />}
                    label="No"
                    color="black"
                  />
                  <FormControlLabel
                    value="maybe"
                    control={<Radio color="primary" />}
                    label="Skip"
                    color="black"
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

      {/* <Dialog open={errorModal} onClose={closeErrorModal}>
        <DialogTitle>{"Incomplete Survey"}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please answer all questions before submitting the survey.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeErrorModal} color="primary">
            Okay
          </Button>
        </DialogActions>
      </Dialog> */}
    </div>
  );
}
