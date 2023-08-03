//@ts-nocheck
"use client";

import { useForm, SubmitHandler } from "react-hook-form";
import axios from "axios";
import { useEffect, useState } from "react";
import { Spinner } from "../components/Spinner";
import Typewriter from "typewriter-effect";
import Container from "../layout/Container";
import Link from "next/link";

type Inputs = {
  question: string;
};

type ChatEntry = {
  role: string;
  content: string;
};

export default function ClientContent({ products }) {
  const [currentAnswer, setCurrentAnswer] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<Inputs>();

  const onSubmit: SubmitHandler<Inputs> = (data) => {
    setIsLoading(true);
    setCurrentAnswer("");
    axios
      .post("/api/chat-query", {
        query: data.question,
      })
      .then(function (response) {
        setCurrentAnswer(response.data.result.answer);
        setIsLoading(false);
      })
      .catch(function (error) {
        setIsLoading(false);
        console.log(error);
      });
    setValue("question", "");
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
              className="bg-emerald-600 px-3 py-2 mt-8 rounded-md text-white hover:bg-emerald-500 mr-5"
            >
              Send
            </button>
          </form>
          {currentAnswer && (
            <div>
              <p className="mt-8 mb-2">
                <strong>Response:</strong>
              </p>
              <div>
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
            </div>
          )}
          {isLoading && (
            <div className="mt-8 flex justify-center">
              <Spinner />
            </div>
          )}
        </div>
        <h4 className="text-2xl mb-8">Our products:</h4>
        <ul className="grid md:grid-cols-3 gap-5">
          {products.map((product, i) => (
            <Link href={`/product/${product.slug}`} key={i}>
              <li className="h-full">
                <div className="p-5 border bg-white h-full max-w-4xl mx-auto rounded-md">
                  <h2 className="text-2xl">
                    <strong>Name:</strong> {product.name}
                  </h2>
                  <p className="text-lg">
                    <strong>Price:</strong> {product.currency} {product.price}
                  </p>
                </div>
              </li>
            </Link>
          ))}
        </ul>
      </Container>
    </main>
  );
}
