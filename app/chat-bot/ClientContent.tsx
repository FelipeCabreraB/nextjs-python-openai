"use client";

import { useForm, SubmitHandler } from "react-hook-form";
import axios from "axios";
import { useState } from "react";
import { Spinner } from "../components/Spinner";
import Container from "../_layout/Container";
import ProductCard from "../components/ProductCard";
import Cookie from "js-cookie";
import { setCookie } from "../_utils/set-cookie";
import { v4 as uuidv4 } from "uuid";
import Typewriter from "typewriter-effect";

type Inputs = {
  question: string;
};

export default function ClientContent({ products }: Products) {
  const [chatHistory, setChatHistory] = useState<{ content: string }[]>([]);
  const [question, setQuestion] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [answer, setAnswer] = useState<string>("");
  const [currentAnswer, setCurrentAnswer] = useState<string>("");

  setCookie();
  const session_id = Cookie.get("session_id");

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
        session_id,
      });
      setChatHistory(response.data?.chat_history);
      setAnswer(response.data?.answer);
      setCurrentAnswer(response.data?.answer);
      setQuestion(response.data?.question);
    } catch (error) {
      console.log(error);
    }
    setIsLoading(false);
    setValue("question", "");
  };

  const clearMemory = async () => {
    Cookie.set("session_id", uuidv4(), { expires: 2 });
    setChatHistory([]);
    setAnswer("");
    setQuestion("");
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
            className="text-primary inline-block text-xl px-5 py-3 rounded-lg bg-secondary hover:bg-opacity-80 transition shadow-md mt-5"
            onClick={clearMemory}
          >
            Start a new conversation
          </button>
          <div className="mt-10">
            {chatHistory.map((entry, i) => (
              <div key={i} className="even:ml-10 even:mb-5 odd:font-bold">
                {entry.content}
              </div>
            ))}
            <p className="font-bold">{question}</p>
            <p className="ml-10">{answer}</p>
          </div>
          {/* <div className="ml-10">
            <Typewriter
              onInit={(typewriter) => {
                typewriter.typeString(answer).start();
              }}
              options={{
                delay: 5,
              }}
            />
          </div> */}

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
