import { useEffect, useState } from "react";
import api from "../services/api";

function CardsPage() {
  const [cards, setCards] = useState([]);
  const [query, setQuery] = useState(""); // For search input
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    async function fetchCards() {
      try {
        const res = await api.get(`/cards?q=${encodeURIComponent(searchTerm)}`);
        setCards(res.data);
      } catch (err) {
        alert("Failed to load cards");
      }
    }

    fetchCards();
  }, [searchTerm]);

  const handleSearch = (e) => {
    e.preventDefault();
    setSearchTerm(query.trim());
  };
  


  return (
    <div className="container">
      <h2>Search Knowledge Cards</h2>

      <form onSubmit={handleSearch} style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
        <input
          type="text"
          placeholder="Search by title or summary..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>

      {cards.length === 0 ? (
        <p>No cards found.</p>
      ) : (
         <div className="card-grid">
          {cards.map((card) => (
            <div key={card.id} className="card">
              <h3>{card.title}</h3>
              <p>{card.summary}</p>
              <p>
                <strong>Tags:</strong> {card.tags.join(", ")}
              </p>
              {card.source_link && (
                <p>
                  <a href={card.source_link} target="_blank" rel="noreferrer">
                    Source
                  </a>
                </p>
              )}
              <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.5rem" }}>
               
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CardsPage;

        