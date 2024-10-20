import React from "react";

const Question = ({ question, onChange }) => {
  // const handleChange = (e) => {
  //   onChange(question.id, e.target.value);
  // };

  return (
    <div className="mb-6">
      <h2 className="text-xl font-bold mb-4">{question.text}</h2>
      <div className="flex space-x-4">
        <label>
          <input
            type="radio"
            name={`question-${question.id}`}
            value="yes"
            // onChange={handleChange}
            className="mr-2"
          />
          Yes
        </label>
        <label>
          <input
            type="radio"
            name={`question-${question.id}`}
            value="no"
            // onChange={handleChange}
            className="mr-2"
          />
          No
        </label>
        <label>
          <input
            type="radio"
            name={`question-${question.id}`}
            value="skip"
            // onChange={handleChange}
            className="mr-2"
          />
          Skip
        </label>
      </div>
    </div>
  );
};

export default Question;
