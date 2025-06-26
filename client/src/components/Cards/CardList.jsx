import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

function CardList() {
  const [cards, setCards] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCards();
  }, []);

  async function fetchCards() {
    try {
      const res = await api.get("/cards");
      setCards(res.data);
    } catch (err) {
      console.error("Failed to fetch cards:", err);
    }
  }

  async function handleDelete(id) {
    if (window.confirm("Are you sure you want to delete this card?")) {
      try {
        await api.delete(`/cards/${id}`);
        setCards((prev) => prev.filter((card) => card.id !== id));
      } catch (err) {
        alert("Failed to delete card");
        console.error(err);
      }
    }
  }

  return (
    <div>
      <h2>Your Knowledge Cards</h2>
      <div className="card-grid">
        {cards.map((card) => (
          <div className="card" key={card.id}>
            <h3>{card.title}</h3>
            <p><strong>Summary:</strong> {card.summary}</p>
            <p><strong>Tags:</strong> {card.tags.join(", ")}</p>
            <p><strong>Source:</strong> <a href={card.source_link} target="_blank" rel="noopener noreferrer">{card.source_link}</a></p>
            <p><strong>Review Score:</strong> {card.review_score}/5</p>
            <p><strong>Last Reviewed:</strong> {new Date(card.last_reviewed).toLocaleString()}</p>
            <p><strong>Next Review Due:</strong> {new Date(card.next_review_due).toLocaleString()}</p>

            <div className="card-actions">
              <button onClick={() => navigate(`/cards/edit/${card.id}`)}>Edit</button>
              <button onClick={() => handleDelete(card.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CardList;
