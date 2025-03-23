import React from "react";

const Question = ({ question, onChange }) => {
  const handleChange = (event) => {
    onChange(question.text, event.target.value); // Pass question text as ID
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-4">
      <h2 className="text-lg font-semibold mb-2">
        Do you think this is disinformation?
      </h2>
      <p className="mb-4">{question.text}</p> {/* Display the comment text */}
      <div className="flex flex-col">
        <label className="inline-flex items-center">
          <input
            type="radio"
            className="mr-2"
            name={question.text} // Ensure all radio buttons are grouped by question text
            value="Yes"
            onChange={handleChange}
          />
          Yes
        </label>
        <label className="inline-flex items-center">
          <input
            type="radio"
            className="mr-2"
            name={question.text} // Ensure all radio buttons are grouped by question text
            value="No"
            onChange={handleChange}
          />
          No
        </label>
        <label className="inline-flex items-center">
          <input
            type="radio"
            className="mr-2"
            name={question.text} // Ensure all radio buttons are grouped by question text
            value="Skip"
            onChange={handleChange}
          />
          Skip
        </label>
      </div>
    </div>
  );
};

export default Question;
