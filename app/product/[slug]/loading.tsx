'use client'
import Image from "next/image";
import { useEffect, useState } from "react";

const Loading = () => {
  const [index, setIndex] = useState<number>(Math.floor(Math.random() * (10 - 1 + 1)) + 1)

  useEffect(() => {
    const interval = setInterval(() => {
      if (index === 10) {
        setIndex(1);
        return;
      }
      setIndex(Math.floor(Math.random() * (10 - 1 + 1)) + 1);
    }, 3000);
    return () => clearInterval(interval);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div className="h-screen flex justify-center items-center">
      <Image
        alt="loading"
        src={`/img/giphy${index}.gif`}
        width={500}
        height={500}
      />
    </div>
  );
};

export default Loading;
