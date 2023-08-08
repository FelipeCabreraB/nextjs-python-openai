//@ts-nocheck

import ProductCard from "@/app/components/ProductCard";
import Container from "@/app/layout/Container";
import axios from "axios";

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

async function getAllProducts() {
  try {
    const res = await fetch("https://api.swell.store/products?limit=1000", {
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
    const response = await axios.post(
      `${process.env.API_BASE_ROUTE}/api/related`,
      {
        product,
      }
    );
    return response.data;
  } catch (error) {
    console.log(error.message);
  }
};

const Product = async ({ params }) => {
  const { slug } = params;
  const { results } = await getData(slug);
  const allProducts = await getAllProducts();

  const product = results[0];
  const products = allProducts.results;

  const related_products = await getRelatedProducts({
    name: product.name,
    description: product.description,
  });

  const relatedProducts = products.filter((product) =>
    related_products.includes(product.id)
  );

  return (
    <>
      <Container className="mb-20">
        <ProductCard product={product} />
        <h2 className="text-2xl mb-8 text-primary mt-10">Related products:</h2>
        <ul className="grid md:grid-cols-3 gap-5">
          {relatedProducts?.map((element) => (
            <ProductCard key={element.id} product={element} />
          ))}
        </ul>
      </Container>
    </>
  );
};

export default Product;
