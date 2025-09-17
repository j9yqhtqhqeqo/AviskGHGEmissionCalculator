import React from "react";

function Home() {
  return (
    <div
      style={{
        fontFamily: "Arial, sans-serif",
        padding: "20px",
        maxWidth: "1200px",
        margin: "0 auto",
      }}
    >
      {/* Header Section */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          marginBottom: "30px",
        }}
      >
        {/* Saxco Logo */}
        <div>
          <img
            src="/saxcologo.jpeg"
            alt="Saxco International"
            style={{ maxWidth: "250px", height: "auto" }}
          />
        </div>

        {/* Title Section */}
        <div style={{ textAlign: "right", flex: 1, marginLeft: "20px" }}>
          <h1
            style={{
              color: "#666",
              fontSize: "36px",
              margin: "0 0 10px 0",
              fontWeight: "normal",
            }}
          >
            Manufacturing and Transportation
          </h1>
          <h2
            style={{
              color: "#666",
              fontSize: "28px",
              margin: "0 0 10px 0",
              fontWeight: "normal",
            }}
          >
            GHG Emissions Calculation Tool
          </h2>
          <p
            style={{
              color: "#666",
              fontSize: "18px",
              margin: "0",
              fontWeight: "normal",
            }}
          >
            Version 1.0
          </p>
        </div>
      </div>

      {/* Content Section */}
      <div style={{ display: "flex", gap: "40px" }}>
        {/* Left Column - Introduction */}
        <div style={{ flex: 1 }}>
          <h3
            style={{
              color: "#2a5783",
              fontSize: "24px",
              marginBottom: "20px",
              fontWeight: "bold",
            }}
          >
            Introduction
          </h3>

          <p
            style={{
              fontSize: "16px",
              lineHeight: "1.5",
              marginBottom: "20px",
              color: "#333",
            }}
          >
            This tool calculates the CO2 emissions from:
          </p>

          <ul
            style={{
              fontSize: "16px",
              lineHeight: "1.5",
              marginBottom: "30px",
              color: "#333",
              paddingLeft: "20px",
            }}
          >
            <li>Manufacturing of containers by suppliers</li>
            <li>Public transport of containers by road, rail, and water.</li>
          </ul>

          <h3
            style={{
              color: "#2a5783",
              fontSize: "24px",
              marginBottom: "20px",
              fontWeight: "bold",
            }}
          >
            Notes
          </h3>

          <div style={{ fontSize: "14px", lineHeight: "1.4", color: "#333" }}>
            <p style={{ marginBottom: "15px" }}>
              * The tool uses default emission factors as well as
              supplier-provided emissions factors, which vary by country.
            </p>
            <p style={{ marginBottom: "15px" }}>
              * The emission factors for transportation activities used in this
              tool come from the UK Dept. for Environment, Food and Rural
              Affairs (DEFRA), the US Environmental Protection Agency (EPA) and
              the Intergovernmental Panel on Climate Change's (IPCC) 2006
              Guidelines for National Greenhouse Gas Inventories.
            </p>

            <p
              style={{
                fontStyle: "italic",
                fontWeight: "bold",
                marginBottom: "15px",
                marginTop: "25px",
              }}
            >
              What data do I need?
            </p>

            <p style={{ marginBottom: "15px" }}>
              Fuel use data are most accurate for calculating CO2 emissions,
              while distance-traveled data are most accurate for calculating CH4
              and N2O emissions. So, for non-public transport sources, the
              recommended approach is to provide both fuel use and distance
              data. Where one type of data is unavailable, the tool uses fuel
              economy information (where available) to convert between these
              data types. Because CO2 contributes most to GHG emissions
              (&gt;95%), companies should first strive to improve their fuel use
              records.
            </p>

            <p style={{ marginBottom: "15px" }}>
              Please note that the emission from on-road freight transport can
              be calculated using vehicle distance or weight-distance data.
            </p>
          </div>
        </div>

        {/* Right Column - Information Box */}
        <div
          style={{
            width: "350px",
            border: "2px solid #333",
            padding: "20px",
            backgroundColor: "#f9f9f9",
          }}
        >
          <p
            style={{
              fontSize: "14px",
              margin: "0 0 15px 0",
              lineHeight: "1.4",
              color: "#333",
            }}
          >
            This tool has been adapted from the prior work of Clear Standards
            Inc. in collaboration with WRI:{" "}
            <em>
              World Resources Institute (2015). GHG Protocol tool for mobile
              combustion. Version 2.6.
            </em>
          </p>

          <p
            style={{
              fontSize: "14px",
              margin: "0",
              lineHeight: "1.4",
              color: "#333",
              textAlign: "center",
              fontWeight: "bold",
            }}
          >
            The Saxco carbon calculator was originally developed by NPV
            Associates. Version 1.0. (2022) )
          </p>

          <p
            style={{
              fontSize: "14px",
              margin: "0",
              lineHeight: "1.4",
              color: "#333",
              textAlign: "center",
              fontWeight: "bold",
            }}
          >
             The latest Web Version is developed by Avisk Analytics. Version 1.0. (2025)
          </p>
        </div>
      </div>
    </div>
  );
}

export default Home;
