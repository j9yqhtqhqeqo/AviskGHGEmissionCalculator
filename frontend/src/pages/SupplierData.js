import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/SupplierData.css";

function SupplierData() {
  // State for region, mode_of_transport, scope, type_of_activity_data, and vehicle type dropdown options
  const [regionOptions, setRegionOptions] = useState([]);
  const [regionLoading, setRegionLoading] = useState(true);
  const [regionError, setRegionError] = useState(null);
  const [motOptions, setMotOptions] = useState([]);
  const [motLoading, setMotLoading] = useState(true);
  const [motError, setMotError] = useState(null);
  const [scopeOptions, setScopeOptions] = useState([]);
  const [scopeLoading, setScopeLoading] = useState(true);
  const [scopeError, setScopeError] = useState(null);
  const [activityTypeOptions, setActivityTypeOptions] = useState([]);
  const [activityTypeLoading, setActivityTypeLoading] = useState(true);
  const [activityTypeError, setActivityTypeError] = useState(null);
  
  // Vehicle type dropdowns per row
  const [vehicleTypeOptions, setVehicleTypeOptions] = useState({});
  const [vehicleTypeLoading, setVehicleTypeLoading] = useState({});
  const [vehicleTypeError, setVehicleTypeError] = useState({});

  // Supplier data state
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

  // Data grid state for activity/transportation data
  const [activityRows, setActivityRows] = useState([
    {
      sourceDescription: "",
      region: "US",
      modeOfTransport: "Water",
      scope: "Scope 3",
      typeOfActivityData: "Weight Distance (e.g. Freight Transport)",
      vehicleType: "Watercraft - Shipping - Large Container Vessel (20000 tonnes)",
      distanceTravelled: "1,000",
      totalWeight: "381.6000",
      numPassengers: "",
      units: "Tonne Mile",
      fuelUsed: "Jet Fuel",
      fuelAmount: "",
      unitOfFuelAmount: "",
    },
  ]);

  const activityColumns = [
    { key: "sourceDescription", label: "Source Description" },
    { key: "region", label: "Region" },
    { key: "modeOfTransport", label: "Mode of Transport" },
    { key: "scope", label: "Scope" },
    { key: "typeOfActivityData", label: "Type of Activity Data" },
    { key: "vehicleType", label: "Vehicle Type" },
    { key: "distanceTravelled", label: "Distance Travelled" },
    { key: "totalWeight", label: "Total Weight of Freight (tonne)" },
    { key: "numPassengers", label: "# of Passengers" },
    { key: "units", label: "Units of Measurement (Tonne Miles)" },
    { key: "fuelUsed", label: "Fuel Used" },
    { key: "fuelAmount", label: "Fuel Amount" },
    { key: "unitOfFuelAmount", label: "Unit of Fuel Amount" },
  ];

  // Fetch vehicle type options for a specific row
  const fetchVehicleTypeOptions = async (rowIdx, region, modeOfTransport) => {
    if (!region || !modeOfTransport) {
      setVehicleTypeOptions((prev) => ({ ...prev, [rowIdx]: [] }));
      return;
    }
    setVehicleTypeLoading((prev) => ({ ...prev, [rowIdx]: true }));
    setVehicleTypeError((prev) => ({ ...prev, [rowIdx]: null }));
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/vehicle_and_size?region=${encodeURIComponent(region)}&mode_of_transport=${encodeURIComponent(modeOfTransport)}`
      );
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      const data = await response.json();
      setVehicleTypeOptions((prev) => ({ ...prev, [rowIdx]: data.vehicle_and_size || [] }));
      setVehicleTypeLoading((prev) => ({ ...prev, [rowIdx]: false }));
    } catch (err) {
      setVehicleTypeError((prev) => ({ ...prev, [rowIdx]: "Failed to load vehicle types." }));
      setVehicleTypeLoading((prev) => ({ ...prev, [rowIdx]: false }));
    }
  };

  const handleActivityCellChange = (rowIdx, key, value) => {
    setActivityRows((prevRows) => {
      const updated = [...prevRows];
      updated[rowIdx] = { ...updated[rowIdx], [key]: value };
      return updated;
    });
  };

  const handleAddActivityRow = () => {
    setActivityRows((prevRows) => [
      ...prevRows,
      {
        sourceDescription: "",
        region: "",
        modeOfTransport: "",
        scope: "",
        typeOfActivityData: "",
        vehicleType: "",
        distanceTravelled: "",
        totalWeight: "",
        numPassengers: "",
        units: "",
        fuelUsed: "",
        fuelAmount: "",
        unitOfFuelAmount: "",
      },
    ]);
  };

  const handleRemoveActivityRow = (rowIdx) => {
    setActivityRows((prevRows) => prevRows.filter((_, idx) => idx !== rowIdx));
  };

  // Fetch suppliers from backend API
  useEffect(() => {
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

  // Fetch region, mode_of_transport, scope, and type_of_activity_data options for dropdowns
  useEffect(() => {
    const fetchRegions = async () => {
      try {
        setRegionLoading(true);
        const response = await fetch("http://127.0.0.1:5000/api/lookup/region");
        if (!response.ok)
          throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        setRegionOptions(data.values || []);
        setRegionLoading(false);
      } catch (err) {
        setRegionError("Failed to load regions.");
        setRegionLoading(false);
      }
    };
    const fetchMot = async () => {
      try {
        setMotLoading(true);
        const response = await fetch(
          "http://127.0.0.1:5000/api/lookup/mode_of_transport"
        );
        if (!response.ok)
          throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        setMotOptions(data.values || []);
        setMotLoading(false);
      } catch (err) {
        setMotError("Failed to load modes of transport.");
        setMotLoading(false);
      }
    };
    const fetchScope = async () => {
      try {
        setScopeLoading(true);
        const response = await fetch("http://127.0.0.1:5000/api/lookup/scope");
        if (!response.ok)
          throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        setScopeOptions(data.values || []);
        setScopeLoading(false);
      } catch (err) {
        setScopeError("Failed to load scopes.");
        setScopeLoading(false);
      }
    };
    const fetchActivityType = async () => {
      try {
        setActivityTypeLoading(true);
        const response = await fetch(
          "http://127.0.0.1:5000/api/lookup/type_of_activity_data"
        );
        if (!response.ok)
          throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        setActivityTypeOptions(data.values || []);
        setActivityTypeLoading(false);
      } catch (err) {
        setActivityTypeError("Failed to load activity types.");
        setActivityTypeLoading(false);
      }
    };
    fetchRegions();
    fetchMot();
    fetchScope();
    fetchActivityType();
  }, []);

  // Effect: fetch vehicle type options when region or modeOfTransport changes for any row
  useEffect(() => {
    activityRows.forEach((row, rowIdx) => {
      if (row.region && row.modeOfTransport) {
        fetchVehicleTypeOptions(rowIdx, row.region, row.modeOfTransport);
      } else {
        setVehicleTypeOptions((prev) => ({ ...prev, [rowIdx]: [] }));
      }
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(activityRows.map(row => ({ region: row.region, modeOfTransport: row.modeOfTransport })))]);

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
                  <option value="">Select Supplier</option>
                  {suppliers.map((supplier, idx) => (
                    <option key={idx} value={supplier}>
                      {supplier}
                    </option>
                  ))}
                </select>
              )}
            </div>
          </div>

          <div className="table-row">
            <div className="table-cell header-cell">Enter Container Weight</div>
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

      <div className="activity-data-grid-container">
        <h2>Transportation/Activity Data</h2>
        <table className="activity-data-grid">
          <thead>
            <tr>
              {activityColumns.map((col) => (
                <th key={col.key}>{col.label}</th>
              ))}
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {activityRows.map((row, rowIdx) => (
              <tr key={rowIdx}>
                {activityColumns.map((col) => (
                  <td key={col.key}>
                    {col.key === "region" ? (
                      regionLoading ? (
                        <div className="loading">Loading...</div>
                      ) : regionError ? (
                        <div className="error">{regionError}</div>
                      ) : (
                        <select
                          className="input-field dropdown"
                          value={row[col.key]}
                          onChange={(e) =>
                            handleActivityCellChange(
                              rowIdx,
                              col.key,
                              e.target.value
                            )
                          }
                        >
                          <option value="">Select Region</option>
                          {regionOptions.map((option, idx) => (
                            <option key={idx} value={option}>
                              {option}
                            </option>
                          ))}
                        </select>
                      )
                    ) : col.key === "modeOfTransport" ? (
                      motLoading ? (
                        <div className="loading">Loading...</div>
                      ) : motError ? (
                        <div className="error">{motError}</div>
                      ) : (
                        <select
                          className="input-field dropdown"
                          value={row[col.key]}
                          onChange={(e) =>
                            handleActivityCellChange(
                              rowIdx,
                              col.key,
                              e.target.value
                            )
                          }
                        >
                          <option value="">Select Mode of Transport</option>
                          {motOptions.map((option, idx) => (
                            <option key={idx} value={option}>
                              {option}
                            </option>
                          ))}
                        </select>
                      )
                    ) : col.key === "scope" ? (
                      scopeLoading ? (
                        <div className="loading">Loading...</div>
                      ) : scopeError ? (
                        <div className="error">{scopeError}</div>
                      ) : (
                        <select
                          className="input-field dropdown"
                          value={row[col.key]}
                          onChange={(e) =>
                            handleActivityCellChange(
                              rowIdx,
                              col.key,
                              e.target.value
                            )
                          }
                        >
                          <option value="">Select Scope</option>
                          {scopeOptions.map((option, idx) => (
                            <option key={idx} value={option}>
                              {option}
                            </option>
                          ))}
                        </select>
                      )
                    ) : col.key === "typeOfActivityData" ? (
                      activityTypeLoading ? (
                        <div className="loading">Loading...</div>
                      ) : activityTypeError ? (
                        <div className="error">{activityTypeError}</div>
                      ) : (
                        <select
                          className="input-field dropdown"
                          value={row[col.key]}
                          onChange={(e) =>
                            handleActivityCellChange(
                              rowIdx,
                              col.key,
                              e.target.value
                            )
                          }
                        >
                          <option value="">Select Type of Activity Data</option>
                          {activityTypeOptions.map((option, idx) => (
                            <option key={idx} value={option}>
                              {option}
                            </option>
                          ))}
                        </select>
                      )
                    ) : col.key === "vehicleType" ? (
                      vehicleTypeLoading[rowIdx] ? (
                        <div className="loading">Loading...</div>
                      ) : vehicleTypeError[rowIdx] ? (
                        <div className="error">{vehicleTypeError[rowIdx]}</div>
                      ) : (
                        <select
                          className="input-field dropdown"
                          value={row[col.key]}
                          onChange={(e) => handleActivityCellChange(rowIdx, col.key, e.target.value)}
                        >
                          <option value="">Select Vehicle Type</option>
                          {(vehicleTypeOptions[rowIdx] || []).map((option, idx) => (
                            <option key={idx} value={option}>{option}</option>
                          ))}
                        </select>
                      )
                    ) : (
                      <input
                        type="text"
                        value={row[col.key]}
                        onChange={(e) =>
                          handleActivityCellChange(
                            rowIdx,
                            col.key,
                            e.target.value
                          )
                        }
                        className="input-field"
                      />
                    )}
                  </td>
                ))}
                <td>
                  <button
                    onClick={() => handleRemoveActivityRow(rowIdx)}
                    disabled={activityRows.length === 1}
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <button className="add-row-button" onClick={handleAddActivityRow}>
          Add Row
        </button>
      </div>
    </div>
  );
}

export default SupplierData;
