import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Register from "./components/auth/Register";
import Login from "./components/auth/login";
import Dashboard from "./components/Dashboard";
import CardsPage from "./components/CardsPage"; // Optional full page
import CardList from "./components/Cards/CardList";
import CardForm from "./components/Cards/CardForm";
import Home from "./components/Home";

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/cards" element={<CardList />} />
          <Route path="/cards/new" element={<CardForm />} />
          <Route path="/cards/edit/:id" element={<CardForm />} />
          <Route path="/cards/all" element={<CardsPage />} /> 
        </Routes>
      </div>
    </Router>
  );
}

export default App;
