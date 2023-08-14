import ClientContent from "./ClientContent";

async function getData() {
  try {
    const headers = new Headers();
    headers.append("Authorization", process.env.SWELL_AUTHORIZATION_KEY || "");
    headers.append("Content-Type", "application/json");

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

const ChatBot = async () => {
  const { results } = await getData();
  return (
    <>
      <ClientContent products={results} />
    </>
  );
};

export default ChatBot;
