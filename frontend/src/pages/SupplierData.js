import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/SupplierData.css";
import * as XLSX from "xlsx";
import {
  getApiUrl,
  isDebugEnabled,
  isConsoleLoggingEnabled,
} from "../config/config";

function SupplierData() {
  const navigate = useNavigate();

  // Activity columns definition
  const activityColumns = [
    { key: "sourceDescription", label: "Source/Description" },
    { key: "region", label: "Region" },
    { key: "modeOfTransport", label: "Mode of Transport" },
    { key: "scope", label: "Scope" },
    { key: "typeOfActivityData", label: "Type of Activity Data" },
    { key: "vehicleType", label: "Vehicle Type" },
    { key: "distanceTravelled", label: "Distance Travelled" },
    { key: "totalWeight", label: "Total Weight of Freight (tonne)" },
    { key: "units", label: "Units of Measurement (Tonne Miles)" },
    { key: "fuelUsed", label: "Fuel Used" },
    { key: "fuelAmount", label: "Fuel Amount" },
    { key: "unitOfFuelAmount", label: "Unit of Fuel Amount" },
  ];

  // Helper function to determine if a field should accept only numerical values
  const isNumericalField = (fieldKey) => {
    return ["distanceTravelled", "fuelAmount", "totalWeight"].includes(
      fieldKey
    );
  };

  // Helper function to format number with commas
  const formatNumberWithCommas = (value) => {
    if (!value || value === "") return "";

    // Convert to string and remove any existing commas
    const stringValue = value.toString().replace(/,/g, "");

    // Only format if it's a valid number
    if (!/^\d*\.?\d*$/.test(stringValue)) return value;

    // Split by decimal point
    const parts = stringValue.split(".");

    // Add commas to the integer part only if it has more than 3 digits
    if (parts[0].length > 3) {
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    // Return formatted number
    return parts.length > 1 ? parts.join(".") : parts[0];
  };

  // Helper function to remove commas for calculation/storage
  const removeCommas = (value) => {
    return value ? value.toString().replace(/,/g, "") : "";
  };

  // Validation rules based on Validations.csv
  const validateActivityData = (rows) => {
    const errors = [];

    rows.forEach((row, index) => {
      const rowNumber = index + 1;

      // Skip empty rows
      if (
        !row.typeOfActivityData &&
        !row.vehicleType &&
        !row.distanceTravelled &&
        !row.fuelUsed &&
        !row.fuelAmount
      ) {
        return;
      }

      // Vehicle Type and Fuel compatibility validations (ERRORS - blocking)
      if (row.typeOfActivityData === "Vehicle Distance (e.g. Road Transport)") {
        // CNG vehicle validations
        if (row.vehicleType && row.vehicleType.includes("CNG")) {
          errors.push({
            row: rowNumber,
            message:
              "Sorry. Emission factors are not available for CNG vehicles based on vehicle distance.",
          });
        }

        // Fuel Unknown validations
        if (row.vehicleType && row.vehicleType.includes("Fuel Unknown")) {
          errors.push({
            row: rowNumber,
            message:
              "Sorry. Emission factors based on vehicle distance are not available when the Fuel Used is not known.",
          });
        }

        // Required fields for Vehicle Distance
        if (!row.vehicleType) {
          errors.push({
            row: rowNumber,
            message: "Please select Vehicle Type",
          });
        }
        if (!row.distanceTravelled) {
          errors.push({
            row: rowNumber,
            message: "Please enter Distance Travelled",
          });
        }
      }

      // Passenger Distance validations
      if (
        row.typeOfActivityData === "Passenger Distance (e.g. Public Transport)"
      ) {
        if (!row.vehicleType) {
          errors.push({
            row: rowNumber,
            message: "Please select Vehicle Type",
          });
        }
        if (!row.distanceTravelled) {
          errors.push({
            row: rowNumber,
            message: "Please enter Distance Travelled",
          });
        }
      }

      // Weight Distance validations
      if (
        row.typeOfActivityData === "Weight Distance (e.g. Freight Transport)"
      ) {
        if (!row.vehicleType) {
          errors.push({
            row: rowNumber,
            message: "Please select Vehicle Type",
          });
        }
        if (!row.distanceTravelled) {
          errors.push({
            row: rowNumber,
            message: "Please enter Distance Travelled",
          });
        }
        if (!row.totalWeight) {
          errors.push({
            row: rowNumber,
            message:
              "Please enter gross weight of vehicle, which includes the weight of both the vehicle and the goods",
          });
        }
        // Note: Informational message about freight transport is handled in getInformationalMessages
      }

      // Fuel Use validations
      if (row.typeOfActivityData === "Fuel Use") {
        if (!row.fuelUsed) {
          errors.push({
            row: rowNumber,
            message: "Please select Fuel Used",
          });
        }
        if (!row.fuelAmount) {
          errors.push({
            row: rowNumber,
            message: "Please enter Fuel Amount",
          });
        }
      }

      // Custom Fuel validations
      if (row.typeOfActivityData === "Custom Fuel") {
        if (!row.fuelUsed) {
          errors.push({
            row: rowNumber,
            message:
              "Please select Fuel Used. This selection allows users to use their own 'custom' emission factors that have been entered into the tool on the 'Settings' tab.",
          });
        }
      }

      // Custom Vehicle validations
      if (row.typeOfActivityData === "Custom Vehicle") {
        if (!row.vehicleType) {
          errors.push({
            row: rowNumber,
            message:
              "Please select Vehicle Type. This selection allows users to use their own 'custom' emission factors that have been entered into the tool on the 'Settings' tab.",
          });
        }
        if (!row.distanceTravelled) {
          errors.push({
            row: rowNumber,
            message: "Please enter Distance Travelled",
          });
        }
      }

      // Fuel Use and Vehicle Distance validations
      if (row.typeOfActivityData === "Fuel Use and Vehicle Distance") {
        if (!row.vehicleType) {
          errors.push({
            row: rowNumber,
            message: "Please select Vehicle Type",
          });
        }
        if (!row.distanceTravelled) {
          errors.push({
            row: rowNumber,
            message: "Please enter Distance Travelled",
          });
        }
        if (!row.fuelUsed) {
          errors.push({
            row: rowNumber,
            message: "Please select Fuel Used",
          });
        }
      }

      // Distance and Unit validations
      if (row.distanceTravelled && !row.units) {
        errors.push({
          row: rowNumber,
          message: "Please select Unit of Distance",
        });
      }
      if (!row.distanceTravelled && row.units) {
        errors.push({
          row: rowNumber,
          message: "Please enter Distance Travelled",
        });
      }

      // Unit of Fuel Amount and Fuel Amount dependency validations
      // Skip fuel validations for Weight Distance activity type as it doesn't require fuel data
      if (
        row.typeOfActivityData !== "Weight Distance (e.g. Freight Transport)"
      ) {
        // If Unit of Fuel Amount is selected, then Fuel Amount must be provided
        if (
          row.unitOfFuelAmount &&
          row.unitOfFuelAmount.trim() &&
          (!row.fuelAmount || !row.fuelAmount.toString().trim())
        ) {
          errors.push({
            row: rowNumber,
            message: "Please enter Fuel Amount",
          });
        }

        // Fuel Used and Fuel Amount dependency
        if (
          row.fuelUsed &&
          row.fuelUsed.trim() &&
          (!row.fuelAmount || !row.fuelAmount.toString().trim())
        ) {
          errors.push({
            row: rowNumber,
            message: "Please enter Fuel Amount",
          });
        }
        if (
          (!row.fuelUsed || !row.fuelUsed.trim()) &&
          row.fuelAmount &&
          row.fuelAmount.toString().trim()
        ) {
          errors.push({
            row: rowNumber,
            message: "Please select Fuel Used",
          });
        }
      }
    });

    return errors;
  };

  // Check for regional-specific warnings
  const getRegionalWarnings = (region, modeOfTransport, scope) => {
    const warnings = [];

    if (region === "Other") {
      warnings.push(
        'The default emission factors for "Other" regions are either global defaults (for CO2 emissions based on fuel use) or from UK DEFRA. These values should only be used in the absence of more specific emission factors.'
      );
    }

    if (region === "UK") {
      warnings.push(
        "The default emission factors are sourced from the UK DEFRA (http://www.defra.gov.uk/environment/business/reporting/pdf/passenger-transport.pdf)."
      );

      if (modeOfTransport === "Road") {
        warnings.push(
          "Sorry. UK-specific emission factors are not available to calculate the CH4 and N2O emissions"
        );
      }
    }

    if (region === "US") {
      warnings.push(
        "The default emission factors are sourced from the US EPA Climate Leaders program or from the UK DEFRA (for air travel only)."
      );
    }

    if (modeOfTransport === "Road" && scope === "Scope 1") {
      warnings.push(
        "Fuel use data are preferred for calculating CO2 emissions. Vehicle distance data are preferred for CH4 and N2O."
      );
    }

    if (modeOfTransport === "Aircraft") {
      warnings.push(
        "Sorry. Emission factors are not available to calculate the CH4 and N2O emissions (which contribute <5% to the total GHG emissions from aircraft). Domestic' flights are < 300 miles/483 km; short-haul flights are ≥ 300 miles/483 km and <700 miles/1126 km, and long haul flights are anything ≥ 700 miles/1126 km."
      );
    }

    return warnings;
  };

  // Get informational messages for the summary page (non-blocking)
  const getInformationalMessages = (rows, region, modeOfTransport, scope) => {
    const messages = [];

    // Regional warnings (these are informational, not errors)
    const regionalMessages = getRegionalWarnings(
      region,
      modeOfTransport,
      scope
    );
    messages.push(...regionalMessages);

    // Activity-specific informational messages
    rows.forEach((row, index) => {
      const rowNumber = index + 1;

      // Skip empty rows
      if (
        !row.typeOfActivityData &&
        !row.vehicleType &&
        !row.distanceTravelled &&
        !row.fuelUsed &&
        !row.fuelAmount
      ) {
        return;
      }

      // Weight Distance informational message
      if (
        row.typeOfActivityData === "Weight Distance (e.g. Freight Transport)"
      ) {
        messages.push({
          row: rowNumber,
          message:
            "Emissions from freight transport can also be calculated using Vehicle distance data.",
        });
      }
    });

    return messages;
  };

  // Helper function to handle numerical input validation with comma formatting
  const handleNumericalInput = (value) => {
    // Handle empty input
    if (value === "") return "";

    // Remove commas for validation
    const cleanValue = removeCommas(value);

    // Allow only digits and one decimal point
    if (/^\d*\.?\d*$/.test(cleanValue)) {
      // Format with commas and return
      return formatNumberWithCommas(cleanValue);
    }

    // If invalid, return the previous valid value (without the last character)
    const previousValue = value.slice(0, -1);
    return formatNumberWithCommas(removeCommas(previousValue));
  };
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
  const [unitsOptions, setUnitsOptions] = useState([]);
  const [unitsLoading, setUnitsLoading] = useState(true);
  const [unitsError, setUnitsError] = useState(null);
  const [fuelOptions, setFuelOptions] = useState([]);
  const [fuelLoading, setFuelLoading] = useState(true);
  const [fuelError, setFuelError] = useState(null);
  const [unitOfFuelAmountOptions, setUnitOfFuelAmountOptions] = useState([]);
  const [unitOfFuelAmountLoading, setUnitOfFuelAmountLoading] = useState(true);
  const [unitOfFuelAmountError, setUnitOfFuelAmountError] = useState(null);

  // Vehicle type dropdowns per row
  const [vehicleTypeOptions, setVehicleTypeOptions] = useState({});
  const [vehicleTypeLoading, setVehicleTypeLoading] = useState({});
  const [vehicleTypeError, setVehicleTypeError] = useState({});

  // Supplier data state
  const [formData, setFormData] = useState({
    supplier: "",
    containerWeight: "",
    numberOfContainers: "",
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
      region: "",
      modeOfTransport: "",
      scope: "",
      typeOfActivityData: "",
      vehicleType: "",
      distanceTravelled: "",
      totalWeight: "",
      units: "",
      fuelUsed: "",
      fuelAmount: "",
      unitOfFuelAmount: "",
    },
    {
      sourceDescription: "",
      region: "",
      modeOfTransport: "",
      scope: "",
      typeOfActivityData: "",
      vehicleType: "",
      distanceTravelled: "",
      totalWeight: "",
      units: "",
      fuelUsed: "",
      fuelAmount: "",
      unitOfFuelAmount: "",
    },
    {
      sourceDescription: "",
      region: "",
      modeOfTransport: "",
      scope: "",
      typeOfActivityData: "",
      vehicleType: "",
      distanceTravelled: "",
      totalWeight: "",
      units: "",
      fuelUsed: "",
      fuelAmount: "",
      unitOfFuelAmount: "",
    },
    {
      sourceDescription: "",
      region: "",
      modeOfTransport: "",
      scope: "",
      typeOfActivityData: "",
      vehicleType: "",
      distanceTravelled: "",
      totalWeight: "",
      units: "",
      fuelUsed: "",
      fuelAmount: "",
      unitOfFuelAmount: "",
    },
    {
      sourceDescription: "",
      region: "",
      modeOfTransport: "",
      scope: "",
      typeOfActivityData: "",
      vehicleType: "",
      distanceTravelled: "",
      totalWeight: "",
      units: "",
      fuelUsed: "",
      fuelAmount: "",
      unitOfFuelAmount: "",
    },
  ]);

  // File upload ref
  const fileInputRef = useRef(null);

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
        `${getApiUrl("vehicleAndSize")}?region=${encodeURIComponent(
          region
        )}&mode_of_transport=${encodeURIComponent(modeOfTransport)}`
      );
      if (!response.ok)
        throw new Error(`HTTP error! Status: ${response.status}`);
      const data = await response.json();
      setVehicleTypeOptions((prev) => ({
        ...prev,
        [rowIdx]: data.vehicle_and_size || [],
      }));
      setVehicleTypeLoading((prev) => ({ ...prev, [rowIdx]: false }));
    } catch (err) {
      setVehicleTypeError((prev) => ({
        ...prev,
        [rowIdx]: "Failed to load vehicle types.",
      }));
      setVehicleTypeLoading((prev) => ({ ...prev, [rowIdx]: false }));
    }
  };

  const handleActivityCellChange = (rowIdx, key, value) => {
    // Apply comma formatting for numerical fields
    let processedValue = value;
    if (isNumericalField(key)) {
      processedValue = handleNumericalInput(value);
    }

    setActivityRows((prevRows) => {
      const updated = [...prevRows];
      updated[rowIdx] = { ...updated[rowIdx], [key]: processedValue };
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

  // Restore data from sessionStorage on component mount
  useEffect(() => {
    const restoreData = () => {
      try {
        // Restore form data
        const savedSupplierData = sessionStorage.getItem("supplierData");
        if (savedSupplierData) {
          const parsedData = JSON.parse(savedSupplierData);
          setFormData(parsedData);
        }

        // Restore activity rows
        const savedActivityData = sessionStorage.getItem("activityData");
        if (savedActivityData) {
          const parsedActivityData = JSON.parse(savedActivityData);
          setActivityRows(parsedActivityData);
        }
      } catch (error) {
        console.error("Error restoring data from sessionStorage:", error);
      }
    };

    restoreData();
  }, []);

  // Fetch suppliers from backend API
  useEffect(() => {
    const fetchSuppliers = async () => {
      try {
        setLoading(true);
        const response = await fetch(getApiUrl("suppliers"));

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setSuppliers(data.suppliers || []);

        // Set default supplier if available and no supplier is already selected
        if (data.suppliers && data.suppliers.length > 0) {
          setFormData((prevState) => ({
            ...prevState,
            supplier: prevState.supplier || data.suppliers[0],
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
        const response = await fetch(getApiUrl("region"));
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
        const response = await fetch(getApiUrl("modeOfTransport"));
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
        const response = await fetch(getApiUrl("scope"));
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
        const response = await fetch(getApiUrl("typeOfActivityData"));
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
    const fetchUnits = async () => {
      try {
        setUnitsLoading(true);
        const response = await fetch(getApiUrl("units"));
        if (!response.ok)
          throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        setUnitsOptions(data.values || []);
        setUnitsLoading(false);
      } catch (err) {
        setUnitsError("Failed to load units.");
        setUnitsLoading(false);
      }
    };
    const fetchFuelTypes = async () => {
      try {
        setFuelLoading(true);
        const response = await fetch(getApiUrl("fuelTypes"));
        if (!response.ok)
          throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        setFuelOptions(data.fuel_types || []);
        setFuelLoading(false);
      } catch (err) {
        setFuelError("Failed to load fuel types.");
        setFuelLoading(false);
      }
    };
    const fetchUnitOfFuelAmount = async () => {
      try {
        setUnitOfFuelAmountLoading(true);
        const response = await fetch(getApiUrl("unitOfFuelAmount"));
        if (!response.ok)
          throw new Error(`HTTP error! Status: ${response.status}`);
        const data = await response.json();
        setUnitOfFuelAmountOptions(data.values || []);
        setUnitOfFuelAmountLoading(false);
      } catch (err) {
        setUnitOfFuelAmountError("Failed to load unit of fuel amount options.");
        setUnitOfFuelAmountLoading(false);
      }
    };
    fetchRegions();
    fetchMot();
    fetchScope();
    fetchActivityType();
    fetchUnits();
    fetchFuelTypes();
    fetchUnitOfFuelAmount();
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
  }, [
    JSON.stringify(
      activityRows.map((row) => ({
        region: row.region,
        modeOfTransport: row.modeOfTransport,
      }))
    ),
  ]);

  // Excel file upload handlers
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type
    const validTypes = [
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", // .xlsx
      "application/vnd.ms-excel", // .xls
    ];

    if (!validTypes.includes(file.type)) {
      alert("Please select a valid Excel file (.xlsx or .xls)");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: "array" });

        // Get the first worksheet
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];

        // Convert to JSON
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        if (jsonData.length < 2) {
          alert(
            "Excel file must contain at least a header row and one data row"
          );
          return;
        }

        // Map Excel columns to our data structure
        const headers = jsonData[0];
        const dataRows = jsonData.slice(1);

        const mappedData = dataRows.map((row) => {
          const rowData = {};
          activityColumns.forEach((col, index) => {
            // Try to match column by name or position
            const headerIndex = headers.findIndex(
              (header) =>
                header &&
                header
                  .toString()
                  .toLowerCase()
                  .includes(col.label.toLowerCase().split(" ")[0])
            );
            const valueIndex = headerIndex !== -1 ? headerIndex : index;

            // Get the raw value from Excel
            const rawValue = row[valueIndex];

            // Only set the value if it's not null, undefined, or empty
            if (
              rawValue !== null &&
              rawValue !== undefined &&
              rawValue !== ""
            ) {
              const stringValue = rawValue.toString().trim();
              // Only assign if the trimmed value is not empty
              if (stringValue !== "") {
                rowData[col.key] = stringValue;
              }
            }
            // If no valid value found, don't set the property at all
            // This prevents empty strings from triggering validation
          });
          return rowData;
        });

        // Filter out completely empty rows
        const filteredData = mappedData.filter((row) =>
          Object.values(row).some((value) => value && value.trim() !== "")
        );

        if (filteredData.length === 0) {
          alert("No valid data found in the Excel file");
          return;
        }

        // Update the activity rows state
        setActivityRows(filteredData);
        alert(
          `Successfully imported ${filteredData.length} rows from Excel file`
        );
      } catch (error) {
        console.error("Error parsing Excel file:", error);
        alert(
          "Error parsing Excel file. Please ensure it is a valid Excel format."
        );
      }
    };

    reader.readAsArrayBuffer(file);

    // Reset the file input
    event.target.value = "";
  };

  const handleExportData = () => {
    try {
      // Filter out completely empty rows
      const dataToExport = activityRows.filter((row) =>
        Object.values(row).some(
          (value) => value && value.toString().trim() !== ""
        )
      );

      if (dataToExport.length === 0) {
        alert("No data to export. Please add some data to the grid first.");
        return;
      }

      // Create headers using the column labels
      const headers = activityColumns.map((col) => col.label);

      // Convert data to array format for Excel
      const excelData = [
        headers, // Header row
        ...dataToExport.map((row) =>
          activityColumns.map((col) => row[col.key] || "")
        ),
      ];

      // Create workbook and worksheet
      const workbook = XLSX.utils.book_new();
      const worksheet = XLSX.utils.aoa_to_sheet(excelData);

      // Auto-size columns
      const colWidths = headers.map((header, index) => {
        const maxLength = Math.max(
          header.length,
          ...dataToExport.map(
            (row) => (row[activityColumns[index].key] || "").toString().length
          )
        );
        return { wch: Math.min(Math.max(maxLength + 2, 10), 50) };
      });
      worksheet["!cols"] = colWidths;

      // Add worksheet to workbook
      XLSX.utils.book_append_sheet(workbook, worksheet, "Transportation Data");

      // Generate filename with current date
      const currentDate = new Date().toISOString().split("T")[0];
      const filename = `transportation_activity_data_${currentDate}.xlsx`;

      // Write and download the file
      XLSX.writeFile(workbook, filename);

      alert(`Successfully exported ${dataToExport.length} rows to ${filename}`);
    } catch (error) {
      console.error("Error exporting data:", error);
      alert("Error exporting data. Please try again.");
    }
  };

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

    // For numerical inputs (containerWeight and numberOfContainers), apply comma formatting
    const isNumericField = ["containerWeight", "numberOfContainers"].includes(
      name
    );

    if (isNumericField) {
      const formattedValue = handleNumericalInput(value);
      setFormData({
        ...formData,
        [name]: formattedValue,
      });

      // Clear validation error if the input is now valid
      if (validationErrors[name]) {
        setValidationErrors({
          ...validationErrors,
          [name]: false,
        });
      }
      return;
    }

    // For non-numeric fields, validate that only numbers, commas, periods, and no spaces are entered
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
        <img
          src="/saxcologo.jpeg"
          alt="Saxco International"
          className="company-logo"
          onError={(e) => {
            console.error("Logo failed to load:", e);
            e.target.style.display = "none";
          }}
          onLoad={() => {
            console.log("Logo loaded successfully");
          }}
        />
        <button
          className="update-summary-button"
          onClick={async () => {
            // Validate activity data (only blocking errors)
            const validationErrors = validateActivityData(activityRows);

            if (validationErrors.length > 0) {
              // Display validation errors
              const errorMessages = validationErrors
                .map((error) => `Row ${error.row}: ${error.message}`)
                .join("\n\n");

              alert(
                `Please correct the following errors before proceeding:\n\n${errorMessages}`
              );
              return;
            }

            // Additional supplier data validations
            const supplierErrors = [];

            if (!formData.supplier || !formData.supplier.trim()) {
              supplierErrors.push("Please select Supplier");
            }

            if (
              !formData.containerWeight ||
              !formData.containerWeight.toString().trim()
            ) {
              supplierErrors.push("Please enter Container Weight");
            }

            if (
              !formData.numberOfContainers ||
              !formData.numberOfContainers.toString().trim()
            ) {
              supplierErrors.push("Please enter Number of Containers");
            }

            if (supplierErrors.length > 0) {
              alert(
                `Please correct the following supplier information errors:\n\n${supplierErrors.join(
                  "\n"
                )}`
              );
              return;
            }

            // Check if at least one activity row has data
            const hasActivityData = activityRows.some(
              (row) =>
                row.typeOfActivityData ||
                row.vehicleType ||
                row.distanceTravelled ||
                row.fuelUsed ||
                row.fuelAmount ||
                row.totalWeight
            );

            if (!hasActivityData) {
              alert(
                "Please enter at least one row of activity data before proceeding."
              );
              return;
            }

            // Send data to compute_ghg_emissions API with all grid data in a single call
            try {
              console.log("Sending all data to compute_ghg_emissions API...");

              // Filter rows that have data
              const rowsWithData = activityRows.filter(
                (row) =>
                  row.typeOfActivityData ||
                  row.vehicleType ||
                  row.distanceTravelled ||
                  row.fuelUsed ||
                  row.fuelAmount ||
                  row.totalWeight
              );

              // Prepare supplier data
              const supplierData = {
                Supplier_and_Container: formData.supplier,
                Container_Weight:
                  parseFloat(removeCommas(formData.containerWeight)) || 0,
                Number_Of_Containers:
                  parseInt(removeCommas(formData.numberOfContainers)) || 0,
              };

              // Prepare activity rows data
              const activityRowsData = rowsWithData.map((row, index) => ({
                Source_Description: row.sourceDescription || "",
                Region: row.region || "",
                Mode_of_Transport: row.modeOfTransport || "",
                Scope: row.scope || "",
                Type_Of_Activity_Data: row.typeOfActivityData || "",
                Vehicle_Type: row.vehicleType || null,
                Distance_Travelled: row.distanceTravelled
                  ? parseFloat(removeCommas(row.distanceTravelled))
                  : null,
                Total_Weight_Of_Freight_InTonne: row.totalWeight
                  ? parseFloat(removeCommas(row.totalWeight))
                  : null,
                Units_of_Measurement: row.units || null,
                Fuel_Used: row.fuelUsed || null,
                Fuel_Amount: row.fuelAmount
                  ? parseFloat(removeCommas(row.fuelAmount))
                  : null,
                Unit_Of_Fuel_Amount: row.unitOfFuelAmount || null,
              }));

              // Combine all data into single API payload
              const apiData = {
                supplier_data: supplierData,
                activity_rows: activityRowsData,
              };

              console.log("Combined API payload:", apiData);
              console.log(
                `Sending ${activityRowsData.length} activity rows with supplier data`
              );

              const response = await fetch(getApiUrl("computeGhgEmissions"), {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify(apiData),
              });

              if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
              }

              const result = await response.json();
              console.log("API response:", result);
              console.log(
                "Successfully sent all data to compute_ghg_emissions API"
              );
            } catch (error) {
              console.error("Error sending data to API:", error);
              alert(`Error processing emission calculations: ${error.message}`);
              return;
            }

            // Collect informational messages for the summary page
            const firstRowWithData = activityRows.find(
              (row) => row.region || row.modeOfTransport || row.scope
            );

            let informationalMessages = [];
            if (firstRowWithData) {
              informationalMessages = getInformationalMessages(
                activityRows,
                firstRowWithData.region,
                firstRowWithData.modeOfTransport,
                firstRowWithData.scope
              );
            }

            // Store data for the summary page
            sessionStorage.setItem("supplierData", JSON.stringify(formData));
            sessionStorage.setItem(
              "activityData",
              JSON.stringify(activityRows)
            );
            sessionStorage.setItem(
              "informationalMessages",
              JSON.stringify(informationalMessages)
            );

            // Navigate to emission summary
            navigate("/emission-summary");
          }}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <div style={{ fontSize: "24px" }}>📊</div>
            <div>Update Emission Summary</div>
          </div>
        </button>
      </div>

      <div className="data-entry-container">
        <h2>Supplier Data</h2>
        <div className="data-table">
          <div className="table-row">
            <div className="table-cell header-cell">Supplier and Container</div>
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
            <div className="table-cell header-cell">Container Weight</div>
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
            <div className="table-cell header-cell"># of Containers</div>
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
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "15px",
          }}
        >
          <h2 style={{ margin: 0 }}>Transportation/Activity Data</h2>
          <div style={{ display: "flex", gap: "10px" }}>
            <input
              ref={fileInputRef}
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileUpload}
              style={{ display: "none" }}
            />
            <button className="upload-data-button" onClick={handleUploadClick}>
              Upload Data
            </button>
            <button className="export-data-button" onClick={handleExportData}>
              Export Data
            </button>
          </div>
        </div>
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
                          onChange={(e) =>
                            handleActivityCellChange(
                              rowIdx,
                              col.key,
                              e.target.value
                            )
                          }
                        >
                          <option value="">Select Vehicle Type</option>
                          {(vehicleTypeOptions[rowIdx] || []).map(
                            (option, idx) => (
                              <option key={idx} value={option}>
                                {option}
                              </option>
                            )
                          )}
                        </select>
                      )
                    ) : col.key === "units" ? (
                      unitsLoading ? (
                        <div className="loading">Loading...</div>
                      ) : unitsError ? (
                        <div className="error">{unitsError}</div>
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
                          <option value="">Select Unit</option>
                          {unitsOptions.map((option, idx) => (
                            <option key={idx} value={option}>
                              {option}
                            </option>
                          ))}
                        </select>
                      )
                    ) : col.key === "fuelUsed" ? (
                      fuelLoading ? (
                        <div className="loading">Loading...</div>
                      ) : fuelError ? (
                        <div className="error">{fuelError}</div>
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
                          <option value="">Select Fuel Type</option>
                          {fuelOptions.map((option, idx) => (
                            <option key={idx} value={option}>
                              {option}
                            </option>
                          ))}
                        </select>
                      )
                    ) : col.key === "unitOfFuelAmount" ? (
                      unitOfFuelAmountLoading ? (
                        <div className="loading">Loading...</div>
                      ) : unitOfFuelAmountError ? (
                        <div className="error">{unitOfFuelAmountError}</div>
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
                          <option value="">Select Unit of Fuel Amount</option>
                          {unitOfFuelAmountOptions.map((option, idx) => (
                            <option key={idx} value={option}>
                              {option}
                            </option>
                          ))}
                        </select>
                      )
                    ) : (
                      <input
                        type="text"
                        value={row[col.key]}
                        onChange={(e) => {
                          let value = e.target.value;
                          if (isNumericalField(col.key)) {
                            value = handleNumericalInput(value);
                          }
                          handleActivityCellChange(rowIdx, col.key, value);
                        }}
                        className="input-field"
                        placeholder={
                          isNumericalField(col.key) ? "Enter number" : ""
                        }
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
