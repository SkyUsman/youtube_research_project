import Content from "@/pages/Content";

const Home = () => {
  return (
    <div className="flex justify-center items-center h-screen w-full bg-crimson">
      <div className="flex flex-col justify-center items-center p-8 gap-5 bg-white rounded-xl 2xl:w-1/3 lg:w-1/2 md:w-2/3 sm:w-2/3 w-5/6 h-fit shadow-md">
        <Content />
      </div>
    </div>
  );
};

export default Home;
