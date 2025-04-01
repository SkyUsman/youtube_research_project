import React from "react";

const Loader = () => (
  <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 z-50">
    <div className="animate-spin rounded-full border-t-4 border-b-4 border-white h-12 w-12"></div>
  </div>
);
export default Loader;
