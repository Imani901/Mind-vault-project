import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    async function fetchSummary() {
      try {
        const res = await api.get("/dashboard/summary");
        console.log("Dashboard summary response:", res.data);
        setSummary(res.data);
      } catch (err) {
        console.error("Error loading dashboard:", err);
      }
    }

    fetchSummary();
  }, []);

  if (!summary || !summary.user) return <p>Loading...</p>; 

  const { user, total_cards, due_today, overdue, top_tags } = summary;

  return (
    <div>
      <h2>Welcome, {user.username}!</h2>
      <p>Email: {user.email}</p>
      

      <div className="dashboard-grid">
        <div className="card">
          <h3>Total Cards</h3>
          <p>{total_cards}</p>
        </div>
        <div className="card">
          <h3>Due Today</h3>
          <p>{due_today}</p>
        </div>
        <div className="card">
          <h3>Overdue</h3>
          <p>{overdue}</p>
        </div>
        <div className="card">
          <h3>Top Tags</h3>
          <p>{top_tags.join(", ") || "No tags yet"}</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
