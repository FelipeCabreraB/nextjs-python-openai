import Image from "next/image";

const loading = () => {
  return (
    <div className="h-screen flex justify-center items-center">
      <Image
        alt="loading"
        src="/img/loading-gif.gif"
        width={500}
        height={500}
      />
    </div>
  );
};

export default loading;
