import React from "react";

const Question = ({ question, onChange }) => {
  const handleChange = (event) => {
    onChange(question.id, event.target.value);
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-4">
      <h2 className="text-lg font-semibold mb-2">{question.text}</h2>
      <input
        type="text"
        className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Your response..."
        onChange={handleChange}
      />
    </div>
  );
};

export default Question;
