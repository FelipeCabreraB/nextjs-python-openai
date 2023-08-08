import Link from "next/link";
import Container from "./layout/Container";

const Home = () => {
  return (
    <Container>
      <nav className="py-5 h-screen grid place-content-center">
        <div className="p-10 shadow-md bg-white rounded-lg">
          <h1 className="text-4xl text-secondary font-bold mb-20">
            Commit Assistant
          </h1>
          <div className="gap-5 flex justify-center items-center">
            <Link href="/chat-bot" className="text-secondary inline-block text-xl px-5 py-3 rounded-lg bg-primary hover:bg-opacity-80 transition shadow-md">Chatbot</Link>
            <Link href="/search" className="text-secondary inline-block text-xl px-5 py-3 rounded-lg bg-primary hover:bg-opacity-80 transition shadow-md">Search</Link>
          </div>
        </div>
      </nav>
    </Container>
  );
};

export default Home;
