import React from "react";

const Loader = () => (
  <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 z-50">
    <div className="animate-spin rounded-full border-t-4 border-b-4 border-white h-12 w-12 sm:h-16 sm:w-16 md:h-20 md:w-20 lg:h-24 lg:w-24"></div>
  </div>
);
export default Loader;
