//@ts-nocheck
"use client";

import { useForm, SubmitHandler } from "react-hook-form";
import axios from "axios";
import { useState } from "react";
import { Spinner } from "../components/Spinner";
import Typewriter from "typewriter-effect";
import Container from "../layout/Container";
import Link from "next/link";
import ProductCard from "../components/ProductCard";

type Inputs = {
  question: string;
};

type ChatEntry = {
  role: string;
  content: string;
};

export default function ClientContent({ products }) {
  const [chatHistory, setChatHistory] = useState<{ content: string }[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<Inputs>();

  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    setIsLoading(true);
    try {
      const response = await axios.post("/api/chat-query", {
        query: data.question,
      });
      setChatHistory(response.data.chat_history);
    } catch (error) {
      console.log(error);
    }
    setIsLoading(false);
    setValue("question", "");
  };

  const clearMemory = async () => {
    try {
      setIsLoading(true);
      const response = await axios.post("/api/chat-query", {
        clear_memory: true,
      });
      setChatHistory(response.data);
    } catch (error) {}
    setIsLoading(false);
  };

  return (
    <main className="my-20">
      <Container>
        <div className="p-5 border bg-white my-10 rounded-md">
          <div className="text-5xl mb-5">
            {process.env.NEXT_PUBLIC_SHOP_NAME}
          </div>
          <form
            onSubmit={(e) => {
              void handleSubmit(onSubmit)(e);
            }}
          >
            <label htmlFor="question" className="block mb-8 text-2xl">
              Question for the assistant:
            </label>
            <input
              type="text"
              id="question"
              placeholder="Write any question about any product..."
              className="border block w-full p-2 rounded-md"
              {...register("question", {
                required: "Question is required",
              })}
            />
            {errors.question && (
              <p className="text-red-600 text-xs">{errors.question.message}</p>
            )}
            <button
              type="submit"
              className="text-secondary inline-block text-xl px-5 py-3 rounded-lg bg-primary hover:bg-opacity-80 transition shadow-md mt-5"
            >
              Send
            </button>
          </form>
          <button
            className="ml-2 text-primary inline-block text-xl px-5 py-3 rounded-lg bg-secondary hover:bg-opacity-80 transition shadow-md mt-5"
            onClick={clearMemory}
          >
            Start a new conversation
          </button>
          <div className="mt-10">
            {chatHistory.map((entry, i) => (
              <p key={i} className="even:ml-10 even:mb-5 odd:font-bold">
                {i === chatHistory.length - 1 ? (
                  <Typewriter
                    onInit={(typewriter) => {
                      typewriter.typeString(entry.content).start();
                    }}
                    options={{
                      delay: 5,
                    }}
                  />
                ) : (
                  entry.content
                )}
              </p>
            ))}
          </div>
          {/* {currentAnswer && (
            <div className="ml-10">
              {
                <Typewriter
                  onInit={(typewriter) => {
                    typewriter.typeString(currentAnswer).start();
                  }}
                  options={{
                    delay: 5,
                  }}
                />
              }
            </div>
          )} */}
          {isLoading && (
            <div className="mt-8 flex justify-center">
              <Spinner />
            </div>
          )}
        </div>
        <h4 className="text-2xl mb-8 text-primary">Our products:</h4>
        <ul className="grid md:grid-cols-3 gap-5">
          {products.map((product, i) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </ul>
      </Container>
    </main>
  );
}
