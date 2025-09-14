import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";

// Import pages
import Home from "./components/Home";
import SupplierData from "./pages/SupplierData";

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="app-nav">
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/supplier-data">Supplier Data</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/supplier-data" element={<SupplierData />} />
          {/* Add future routes here */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
