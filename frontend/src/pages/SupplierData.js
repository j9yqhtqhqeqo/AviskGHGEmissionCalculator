import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/SupplierData.css";

function SupplierData() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    supplier: "",
    containerWeight: "530",
    numberOfContainers: "720,000",
  });
  const [suppliers, setSuppliers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [validationErrors, setValidationErrors] = useState({
    containerWeight: false,
    numberOfContainers: false,
  });

  useEffect(() => {
    // Fetch suppliers from backend API
    const fetchSuppliers = async () => {
      try {
        setLoading(true);
        const response = await fetch("http://127.0.0.1:5000/api/suppliers");

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setSuppliers(data.suppliers || []);

        // Set default supplier if available
        if (data.suppliers && data.suppliers.length > 0) {
          setFormData((prevState) => ({
            ...prevState,
            supplier: data.suppliers[0],
          }));
        }

        setLoading(false);
      } catch (err) {
        console.error("Error fetching suppliers:", err);
        setError("Failed to load suppliers. Please try again later.");
        setLoading(false);
      }
    };

    fetchSuppliers();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;

    // For supplier dropdown, we just update the value
    if (name === "supplier") {
      setFormData({
        ...formData,
        [name]: value,
      });
      return;
    }

    // For numerical inputs, validate that only numbers, commas, periods, and no spaces are entered
    const numericRegex = /^[0-9,.]*$/;

    if (numericRegex.test(value) || value === "") {
      setFormData({
        ...formData,
        [name]: value,
      });

      // Clear validation error if the input is now valid
      if (validationErrors[name]) {
        setValidationErrors({
          ...validationErrors,
          [name]: false,
        });
      }
    } else {
      // Set validation error but don't update the form data
      setValidationErrors({
        ...validationErrors,
        [name]: true,
      });
    }
  };

  const handleActivityDataClick = () => {
    // Navigate to activity data page (to be created later)
    navigate("/activity-data");
  };

  return (
    <div className="supplier-data-container">
      <div className="logo-container">
        <picture>
          <source srcSet="/saxco-logo.svg" type="image/svg+xml" />
          <img
            src="/saxco-logo.png"
            alt="Saxco International"
            className="company-logo"
          />
        </picture>
      </div>

      <div className="instructions-container">
        <h1>Instructions</h1>
        <p>
          Select the{" "}
          <span className="highlight">Supplier - Container - Location</span>{" "}
          then enter the container weight and # of total containers.
        </p>
      </div>

      <div className="data-entry-container">
        <h2>Enter Supplier Data</h2>
        <div className="data-table">
          <div className="table-row">
            <div className="table-cell header-cell">
              Select Supplier and Container
            </div>
            <div className="table-cell">
              {loading ? (
                <div className="loading">Loading suppliers...</div>
              ) : error ? (
                <div className="error">{error}</div>
              ) : (
                <select
                  name="supplier"
                  value={formData.supplier}
                  onChange={handleChange}
                  className="input-field dropdown"
                >
                  {suppliers.map((supplier, index) => (
                    <option key={index} value={supplier}>
                      {supplier}
                    </option>
                  ))}
                </select>
              )}
            </div>
          </div>

          <div className="table-row">
            <div className="table-cell header-cell">
              Enter Container (bottle/can) Weight (g)
            </div>
            <div className="table-cell">
              <input
                type="text"
                name="containerWeight"
                value={formData.containerWeight}
                onChange={handleChange}
                className={`input-field ${
                  validationErrors.containerWeight ? "input-error" : ""
                }`}
                placeholder="Enter numbers only"
                aria-label="Container weight in grams"
              />
              {validationErrors.containerWeight && (
                <div className="error-message">Please enter numbers only</div>
              )}
            </div>
          </div>

          <div className="table-row">
            <div className="table-cell header-cell">Enter # of Containers</div>
            <div className="table-cell">
              <input
                type="text"
                name="numberOfContainers"
                value={formData.numberOfContainers}
                onChange={handleChange}
                className={`input-field ${
                  validationErrors.numberOfContainers ? "input-error" : ""
                }`}
                placeholder="Enter numbers only"
                aria-label="Number of containers"
              />
              {validationErrors.numberOfContainers && (
                <div className="error-message">Please enter numbers only</div>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="navigation-container">
        <p>Proceed to "Activity Data" to enter transportation data.</p>
        <button
          className="activity-data-button"
          onClick={handleActivityDataClick}
        >
          Enter Activity Data
        </button>
      </div>
    </div>
  );
}

export default SupplierData;
