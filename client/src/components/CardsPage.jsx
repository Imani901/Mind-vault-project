import { useEffect, useState } from "react";
import api from "../services/api";

function CardsPage() {
  const [cards, setCards] = useState([]);
  const [form, setForm] = useState({ title: "", summary: "", tags: "", source_link: "" });

  useEffect(() => {
    async function fetchCards() {
      try {
        const res = await api.get("/cards");
        setCards(res.data);
      } catch (err) {
        alert("Failed to load cards");
      }
    }

    fetchCards();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await api.post("/cards", {
        ...form,
        tags: form.tags.split(",").map(tag => tag.trim()),
      });
      setCards([...cards, res.data]);
      setForm({ title: "", summary: "", tags: "", source_link: "" });
    } catch (err) {
      alert("Failed to create card");
    }
  }

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  return (
    <div>
      <h2>Create Knowledge Card</h2>
      <form onSubmit={handleSubmit}>
        <input name="title" placeholder="Title" value={form.title} onChange={handleChange} />
        <textarea name="summary" placeholder="Summary" value={form.summary} onChange={handleChange} />
        <input name="tags" placeholder="Tags (comma-separated)" value={form.tags} onChange={handleChange} />
        <input name="source_link" placeholder="Source Link" value={form.source_link} onChange={handleChange} />
        <button type="submit">Add Card</button>
      </form>

      <h2>Your Cards</h2>
      <ul>
        {cards.map(card => (
          <li key={card.id}>
            <strong>{card.title}</strong> - {card.summary}
            <br />
            Tags: {card.tags.join(", ")}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CardsPage;
