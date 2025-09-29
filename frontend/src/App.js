import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useLocation,
} from "react-router-dom";
import "./App.css";

// Import pages
import Login from "./pages/Login";
import Home from "./components/Home";
import SupplierData from "./pages/SupplierData";
import EmissionSummary from "./pages/EmissionSummary";

// Navigation component that conditionally renders
function AppNavigation() {
  const location = useLocation();
  const hideNavPaths = ["/", "/login"];

  if (hideNavPaths.includes(location.pathname)) {
    return null;
  }

  return (
    <nav className="app-nav">
      <ul>
        <li>
          <Link to="/home">Home</Link>
        </li>
        <li>
          <Link to="/supplier-data">Supplier Data</Link>
        </li>
        <li>
          <Link to="/emission-summary">Emission Summary</Link>
        </li>
        <li>
          <Link to="/login">Logout</Link>
        </li>
      </ul>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <AppNavigation />

        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/home" element={<Home />} />
          <Route path="/supplier-data" element={<SupplierData />} />
          <Route path="/emission-summary" element={<EmissionSummary />} />
          {/* Add future routes here */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
