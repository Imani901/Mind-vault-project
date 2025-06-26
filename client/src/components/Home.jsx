// src/components/Home.jsx
import { useEffect, useState } from "react";
import api from "../services/api";

function Home() {
  const [cards, setCards] = useState([]);

  useEffect(() => {
    async function fetchPublicCards() {
      try {
        const res = await api.get("/cards/public");
        setCards(res.data);
      } catch (err) {
        console.error("Failed to load public cards", err);
      }
    }

    fetchPublicCards();
  }, []);

  return (
    <div>
      <h2>Welcome to MindVault</h2>
      <p>Explore some example cards below:</p>
      <div className="card-grid">
        {cards.map((card) => (
          <div key={card.id} className="card">
            <h3>{card.title}</h3>
            <p><strong>Summary:</strong> {card.summary}</p>
            <p><strong>Tags:</strong> {card.tags}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
