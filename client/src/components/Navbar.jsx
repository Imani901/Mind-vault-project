import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("token");
    navigate("/login");
  }

  const loggedIn = !!localStorage.getItem("token");

  return (
    <nav className="navbar">
      <div className="container">
        <h1>MindVault</h1>
        <div>
          <Link to="/">Home</Link>
          {loggedIn ? (
            <>
              <Link to="/dashboard">Dashboard</Link>
              <Link to="/cards">Card List</Link> {/* ✅ Add this */}
              <Link to="/cards/new">New Card</Link>
              <button onClick={handleLogout}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
