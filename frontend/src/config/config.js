/**
 * Frontend configuration for the GHG Emission Calculator
 */

// Environment-based configuration
const environment = process.env.NODE_ENV || "development";

const config = {
  development: {
    api: {
      baseUrl: process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:5002",
      timeout: 30000, // 30 seconds
      endpoints: {
        // Lookup endpoints
        lookup: "/api/lookup",
        scope: "/api/lookup/scope",
        unitOfFuelAmount: "/api/lookup/unit_of_fuel_amount",

        // Specific lookup endpoints
        region: "/api/lookup/region",
        modeOfTransport: "/api/lookup/mode_of_transport",
        typeOfActivityData: "/api/lookup/type_of_activity_data",
        units: "/api/lookup/units",

        // Data endpoints
        suppliers: "/api/suppliers",
        fuelTypes: "/api/fuel_types",
        vehicleAndSize: "/api/vehicle_and_size",
        unitConversion: "/api/unit_conversion",

        // Emission calculation
        computeGhgEmissions: "/api/compute_ghg_emissions",

        // Reference data endpoints
        efFuelUseCo2: "/api/ef_fuel_use_co2",
        efFuelUseCh4N2o: "/api/ef_fuel_use_ch4_n2o",
        efRoad: "/api/ef_road",
        efFreightCo2: "/api/ef_freight_co2",
        efFreightCh4No2: "/api/ef_freight_ch4_no2",
        ef: "/api/ef",
        sourceProductMatrix: "/api/source_product_matrix",
      },
    },
    app: {
      name: "Avisk GHG Emission Calculator",
      version: "1.0.0",
      enableDebug: true,
      enableConsoleLogging: true,
    },
    ui: {
      defaultItemsPerPage: 10,
      maxUploadSizeMB: 10,
      supportedFileTypes: [".xlsx", ".xls"],
      autoSaveInterval: 30000, // 30 seconds
    },
  },

  production: {
    api: {
      baseUrl:
        process.env.REACT_APP_API_BASE_URL || "https://api.yourdomain.com",
      timeout: 60000, // 60 seconds
      endpoints: {
        // Same endpoints as development
        lookup: "/api/lookup",
        scope: "/api/lookup/scope",
        unitOfFuelAmount: "/api/lookup/unit_of_fuel_amount",
        region: "/api/lookup/region",
        modeOfTransport: "/api/lookup/mode_of_transport",
        typeOfActivityData: "/api/lookup/type_of_activity_data",
        units: "/api/lookup/units",
        suppliers: "/api/suppliers",
        fuelTypes: "/api/fuel_types",
        vehicleAndSize: "/api/vehicle_and_size",
        unitConversion: "/api/unit_conversion",
        computeGhgEmissions: "/api/compute_ghg_emissions",
        efFuelUseCo2: "/api/ef_fuel_use_co2",
        efFuelUseCh4N2o: "/api/ef_fuel_use_ch4_n2o",
        efRoad: "/api/ef_road",
        efFreightCo2: "/api/ef_freight_co2",
        efFreightCh4No2: "/api/ef_freight_ch4_no2",
        ef: "/api/ef",
        sourceProductMatrix: "/api/source_product_matrix",
      },
    },
    app: {
      name: "Avisk GHG Emission Calculator",
      version: "1.0.0",
      enableDebug: false,
      enableConsoleLogging: false,
    },
    ui: {
      defaultItemsPerPage: 20,
      maxUploadSizeMB: 50,
      supportedFileTypes: [".xlsx", ".xls"],
      autoSaveInterval: 60000, // 60 seconds
    },
  },

  testing: {
    api: {
      baseUrl: process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:5003",
      timeout: 10000, // 10 seconds
      endpoints: {
        // Same endpoints as development
        lookup: "/api/lookup",
        scope: "/api/lookup/scope",
        unitOfFuelAmount: "/api/lookup/unit_of_fuel_amount",
        region: "/api/lookup/region",
        modeOfTransport: "/api/lookup/mode_of_transport",
        typeOfActivityData: "/api/lookup/type_of_activity_data",
        units: "/api/lookup/units",
        suppliers: "/api/suppliers",
        fuelTypes: "/api/fuel_types",
        vehicleAndSize: "/api/vehicle_and_size",
        unitConversion: "/api/unit_conversion",
        computeGhgEmissions: "/api/compute_ghg_emissions",
        efFuelUseCo2: "/api/ef_fuel_use_co2",
        efFuelUseCh4N2o: "/api/ef_fuel_use_ch4_n2o",
        efRoad: "/api/ef_road",
        efFreightCo2: "/api/ef_freight_co2",
        efFreightCh4No2: "/api/ef_freight_ch4_no2",
        ef: "/api/ef",
        sourceProductMatrix: "/api/source_product_matrix",
      },
    },
    app: {
      name: "Avisk GHG Emission Calculator (Test)",
      version: "1.0.0",
      enableDebug: true,
      enableConsoleLogging: true,
    },
    ui: {
      defaultItemsPerPage: 5,
      maxUploadSizeMB: 5,
      supportedFileTypes: [".xlsx", ".xls"],
      autoSaveInterval: 10000, // 10 seconds
    },
  },
};

// Get current configuration based on environment
const currentConfig = config[environment] || config.development;

// Helper functions
export const getApiUrl = (endpoint) => {
  return `${currentConfig.api.baseUrl}${
    currentConfig.api.endpoints[endpoint] || endpoint
  }`;
};

export const getFullApiUrl = (path) => {
  return `${currentConfig.api.baseUrl}${path}`;
};

export const isDebugEnabled = () => {
  return currentConfig.app.enableDebug;
};

export const isConsoleLoggingEnabled = () => {
  return currentConfig.app.enableConsoleLogging;
};

// Export configuration object
export default currentConfig;
