import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../../services/api";

function CardForm() {
  const [form, setForm] = useState({
    title: "",
    summary: "",
    tags: [],
    source_link: ""
  });

  const navigate = useNavigate();
  const { id } = useParams(); // If present, we're editing

  useEffect(() => {
    if (id) {
      // fetch card for editing
      api.get(`/cards`)
        .then(res => {
          const card = res.data.find(c => c.id === parseInt(id));
          if (card) {
            setForm({
              title: card.title,
              summary: card.summary,
              tags: card.tags,
              source_link: card.source_link
            });
          }
        })
        .catch(err => {
          console.error("Failed to fetch card", err);
        });
    }
  }, [id]);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm({ ...form, [name]: name === "tags" ? value.split(",") : value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      if (id) {
        await api.patch(`/cards/${id}`, form);
      } else {
        await api.post("/cards", form);
      }
      navigate("/cards");
    } catch (err) {
      alert("Failed to save card");
      console.error(err);
    }
  }

  return (
    <div>
      <h2>{id ? "Edit Card" : "New Card"}</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="title"
          placeholder="Title"
          value={form.title}
          onChange={handleChange}
          required
        />
        <textarea
          name="summary"
          placeholder="Summary"
          value={form.summary}
          onChange={handleChange}
          required
        />
        <input
          name="tags"
          placeholder="Tags (comma-separated)"
          value={form.tags.join(",")}
          onChange={handleChange}
        />
        <input
          name="source_link"
          placeholder="Source link"
          value={form.source_link}
          onChange={handleChange}
        />
        <button type="submit">{id ? "Update" : "Create"}</button>
      </form>
    </div>
  );
}

export default CardForm;
