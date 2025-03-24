import Content from "@/pages/Content";

const Home = () => {
  return (
    <div className="flex justify-center items-center h-screen w-full bg-crimson">
      <div className="flex flex-col justify-center items-center p-8 gap-5 bg-white rounded-xl w-1/3 h-fit shadow-md">
        <Content />
      </div>
    </div>
  );
};

export default Home;
