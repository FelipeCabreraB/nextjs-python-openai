import ClientContent from "./ClientContent";

const headers = new Headers();
headers.append("Authorization", process.env.SWELL_AUTHORIZATION_KEY || "");
headers.append("Content-Type", "application/json");

async function getData() {
  try {
    const res = await fetch("https://api.swell.store/products?limit=1000", {
      method: "get",
      headers: headers,
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
