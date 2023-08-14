"use client";

import { useForm, SubmitHandler } from "react-hook-form";
import axios from "axios";
import { useEffect, useState } from "react";
import { Spinner } from "../components/Spinner";
import Container from "../_layout/Container";
import ProductCard from "../components/ProductCard";

type Inputs = {
  question: string;
  search_term: string;
};

export default function ClientContent({ products }: Products) {
  const [searchedProducts, setSearchedProducts] = useState<Product[]>();
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [searchInput, setSearchInput] = useState<string>("");
  const [noResult, setNoResult] = useState<boolean>(false);

  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<Inputs>();

  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    setIsLoading(true);
    setSearchedProducts(undefined);
    setSearchInput("");
    setNoResult(false);

    try {
      const response = await axios.post("/api/search", {
        search_term: data.search_term,
      });
      setSearchedProducts(
        products.filter((product) => response.data.includes(product.id))
      );
      setIsLoading(false);
      setSearchInput(data.search_term);
    } catch (error) {
      setIsLoading(false);
      console.log(error);
    } finally {
      setValue("search_term", "");
    }
  };

  useEffect(() => {
    searchedProducts?.length === 0 && setNoResult(true);
  }),
    [searchedProducts, noResult];

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
              Search:
            </label>
            <input
              type="text"
              id="search_term"
              placeholder="Search..."
              className="border block w-full p-2 rounded-md"
              {...register("search_term", {
                required: "Search term is required",
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
          {searchedProducts && (
            <div>
              {noResult ? (
                <p className="mt-8 mb-2">
                  Sorry, we can`t find any product. Please try again with other.
                </p>
              ) : (
                <p className="mt-8 mb-2">
                  <strong>
                    Response for{" "}
                    <span className="uppercase">{searchInput}</span>
                  </strong>
                </p>
              )}
              <div>
                <ul className="grid md:grid-cols-3 gap-5">
                  {searchedProducts?.map((product, i) => (
                    <ProductCard key={i} product={product} />
                  ))}
                </ul>
              </div>
            </div>
          )}
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
