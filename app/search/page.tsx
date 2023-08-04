//@ts-nocheck

import ClientContent from "./ClientContent";

async function getData() {
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

const Search = async () => {
  const { results } = await getData();
  return (
    <>
      <ClientContent products={results} />
    </>
  );
};

export default Search;
