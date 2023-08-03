//@ts-nocheck

import Container from "@/app/layout/Container";
import axios from "axios";
import Link from "next/link";

async function getData(slug: string) {
  try {
    const res = await fetch(`https://api.swell.store/products?slug=${slug}`, {
      method: "get",
      headers: {
        Authorization: process.env.SWELL_AUTHORIZATION_KEY,
        "Content-Type": "application/json",
      },
    });
    const products = await res.json();
    return products;
  } catch (error) {
    return [];
  }
}

const getRelatedProducts = async (product) => {
  try {
    const response = await axios.post("http://localhost:8000/api/related", {
      product,
    });
    return response.data;
  } catch (error) {
    console.log(error.message);
  }
};

const Product = async ({ params }) => {
  const { slug } = params;
  const { results } = await getData(slug);
  const product = results[0];

  const related_products = await getRelatedProducts({
    name: product.name,
    description: product.description,
  });

  return (
    <>
      <Container>
        <div className="p-5 border bg-white max-w-4xl mx-auto rounded-md my-10">
          <h2 className="text-2xl">
            <strong>Name:</strong> {product.name}
          </h2>
          <p className="text-lg">
            <strong>Price:</strong> {product.currency} {product.price}
          </p>
        </div>

        <h2 className="text-2xl mb-4">Related products:</h2>
        <ul className="grid md:grid-cols-3 gap-5">
          {related_products?.map((product, i) => (
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
    </>
  );
};

export default Product;
