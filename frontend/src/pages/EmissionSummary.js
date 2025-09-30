import React, { useState, useEffect } from "react";
import "../styles/EmissionSummary.css";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

function EmissionSummary() {
  const [informationalMessages, setInformationalMessages] = useState([]);
  const [supplierData, setSupplierData] = useState(null);
  const [emissionResults, setEmissionResults] = useState(null);

  useEffect(() => {
    // Retrieve all data from sessionStorage
    const storedMessages = sessionStorage.getItem("informationalMessages");
    const storedSupplierData = sessionStorage.getItem("supplierData");
    const storedEmissionResults = sessionStorage.getItem("emissionResults");

    if (storedMessages) {
      try {
        const messages = JSON.parse(storedMessages);
        setInformationalMessages(messages);
      } catch (error) {
        console.error("Error parsing informational messages:", error);
      }
    }

    if (storedSupplierData) {
      try {
        const supplier = JSON.parse(storedSupplierData);
        setSupplierData(supplier);
      } catch (error) {
        console.error("Error parsing supplier data:", error);
      }
    }

    if (storedEmissionResults) {
      try {
        const results = JSON.parse(storedEmissionResults);
        setEmissionResults(results);
      } catch (error) {
        console.error("Error parsing emission results:", error);
      }
    }
  }, []);

  // Calculate totals from actual data using new API response structure
  const calculateTotals = () => {
    if (!emissionResults) {
      return {
        totalManufacturingEmissions: 0,
        totalTransportEmissions: 0,
        totalEmissions: 0,
        totalMaterialWeight: 0,
        supplierEmissionFactor: 0,
      };
    }

    // Use values from API instead of recalculating, with proper null checking
    const totalMaterialWeight =
      emissionResults?.manufacturing_details?.total_material_weight_tonnes || 0;
    const supplierEmissionFactor =
      emissionResults?.manufacturing_details?.supplier_emission_factor || 0;
    const manufacturingEmissions =
      emissionResults?.manufacturing_emissions || 0;

    // Use transport_emissions.co2 from the new API response
    const transportEmissions = emissionResults?.transport_emissions?.co2 || 0;

    // Use total_emissions from API instead of calculating on frontend
    const totalEmissions = emissionResults?.total_emissions || 0;

    return {
      totalManufacturingEmissions: manufacturingEmissions,
      totalTransportEmissions: transportEmissions,
      totalEmissions: totalEmissions,
      totalMaterialWeight: totalMaterialWeight,
      supplierEmissionFactor: supplierEmissionFactor,
    };
  };

  const totals = calculateTotals();

  // Calculate transport emissions breakdown using new API response structure
  const getTransportEmissions = () => {
    if (
      !emissionResults?.transport_emissions?.summary_by_transport_scope_activity
    ) {
      return {
        fuel: { co2: 0, ch4: 0, n2o: 0, biofuel: 0 },
        distance: { co2: 0, ch4: 0, n2o: 0, biofuel: 0 },
        byMode: {
          road: { co2: 0, ch4: 0, n2o: 0, biofuel: 0 },
          rail: { co2: 0, ch4: 0, n2o: 0, biofuel: 0 },
          water: { co2: 0, ch4: 0, n2o: 0, biofuel: 0 },
        },
      };
    }

    const summaryData =
      emissionResults.transport_emissions.summary_by_transport_scope_activity;

    // Initialize totals for fuel vs distance based calculations
    let fuelEmissions = { co2: 0, ch4: 0, n2o: 0, biofuel: 0 };
    let distanceEmissions = { co2: 0, ch4: 0, n2o: 0, biofuel: 0 };

    // Initialize totals by mode of transport
    let byMode = {
      road: { co2: 0, ch4: 0, n2o: 0, biofuel: 0 },
      rail: { co2: 0, ch4: 0, n2o: 0, biofuel: 0 },
      water: { co2: 0, ch4: 0, n2o: 0, biofuel: 0 },
    };

    // Process the summary data to aggregate by activity type and mode
    Object.keys(summaryData).forEach((modeOfTransport) => {
      const modeData = summaryData[modeOfTransport];
      const modeKey = modeOfTransport.toLowerCase();

      // Initialize mode if not exists
      if (!byMode[modeKey]) {
        byMode[modeKey] = { co2: 0, ch4: 0, n2o: 0, biofuel: 0 };
      }

      Object.keys(modeData).forEach((scope) => {
        const scopeData = modeData[scope];

        Object.keys(scopeData).forEach((activityType) => {
          const activityData = scopeData[activityType];
          const co2Emissions = activityData.CO2?.total_emissions || 0;

          // Add to activity type totals
          if (activityType === "Fuel") {
            fuelEmissions.co2 += co2Emissions;
          } else if (activityType === "Distance") {
            distanceEmissions.co2 += co2Emissions;
          }

          // Add to mode totals
          byMode[modeKey].co2 += co2Emissions;
        });
      });
    });

    return {
      fuel: fuelEmissions,
      distance: distanceEmissions,
      byMode: byMode,
    };
  };

  const transportEmissions = getTransportEmissions();

  // Export PDF function
  const exportToPDF = async () => {
    try {
      console.log("Starting PDF export...");

      // Hide the export button
      const exportButton = document.querySelector(".export-pdf-button");
      if (exportButton) {
        exportButton.style.display = "none";
      }

      // Create a simplified version for PDF
      const element = document.querySelector(".emission-summary-container");
      if (!element) {
        console.error("Could not find emission-summary-container");
        alert("Could not find content to export");
        return;
      }

      // Create a print-friendly container
      const printContainer = document.createElement("div");
      printContainer.style.cssText = `
        position: absolute;
        left: -9999px;
        top: 0;
        width: 800px;
        padding: 20px;
        background-color: white;
        font-family: Arial, sans-serif;
        color: black;
      `;

      // Add header with logo
      const header = document.createElement("div");
      header.style.cssText = `
        display: flex;
        justify-content: flex-start;
        margin-bottom: 30px;
      `;

      const logo = document.createElement("img");
      logo.src = "/saxcologo.jpeg";
      logo.alt = "Saxco International";
      logo.style.cssText = "max-width: 150px; height: auto;";
      header.appendChild(logo);
      printContainer.appendChild(header);

      // Add Total GHG Emissions Box (simplified version)
      const totalBox = document.createElement("div");
      const bgColor = (() => {
        if (totals.totalEmissions === 0) return "#4caf50";
        if (totals.totalEmissions <= 1000) return "#fff9c4";
        if (totals.totalEmissions <= 2000) return "#9e9e9e";
        if (totals.totalEmissions <= 3000) return "#757575";
        if (totals.totalEmissions <= 4000) return "#616161";
        if (totals.totalEmissions <= 5000) return "#424242";
        return "#303030";
      })();

      const textColor =
        totals.totalEmissions <= 1000 && totals.totalEmissions > 0
          ? "#333"
          : "white";

      totalBox.style.cssText = `
        display: flex;
        background-color: ${bgColor};
        border: 2px solid ${
          totals.totalEmissions === 0
            ? "#66bb6a"
            : totals.totalEmissions <= 1000
            ? "#f9a825"
            : "#757575"
        };
        border-radius: 12px;
        margin-bottom: 30px;
        min-height: 120px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      `;

      const labelDiv = document.createElement("div");
      labelDiv.style.cssText = `
        background-color: transparent;
        padding: 20px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        color: ${textColor};
        display: flex;
        align-items: center;
        justify-content: center;
        border-right: 2px solid ${
          totals.totalEmissions === 0
            ? "#66bb6a"
            : totals.totalEmissions <= 1000
            ? "#f9a825"
            : "#757575"
        };
        min-width: 200px;
      `;
      labelDiv.innerHTML =
        "🌍 Total GHG Emissions<br/>(metric tonnes<br/>CO₂e)";

      const valueDiv = document.createElement("div");
      valueDiv.style.cssText = `
        background-color: transparent;
        padding: 20px 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: ${textColor};
        flex-direction: column;
        flex: 1;
      `;

      const mainValue = document.createElement("div");
      mainValue.style.cssText =
        "font-size: 28px; font-weight: bold; margin-bottom: 5px;";
      mainValue.textContent = totals.totalEmissions.toFixed(2);

      const subValue = document.createElement("div");
      subValue.style.cssText = "font-size: 14px; opacity: 0.9;";
      subValue.textContent = "metric tonnes CO₂e";

      const statusText = document.createElement("div");
      statusText.style.cssText =
        "font-size: 12px; margin-top: 5px; opacity: 0.8;";
      statusText.textContent = (() => {
        if (totals.totalEmissions === 0) return "No Emissions Calculated 🌱";
        if (totals.totalEmissions <= 1000)
          return "Good Industrial Performance 🌿";
        if (totals.totalEmissions <= 2000)
          return "Moderate Industrial Impact 🔲";
        if (totals.totalEmissions <= 3000) return "High Industrial Impact ⬛";
        if (totals.totalEmissions <= 4000)
          return "Very High Industrial Impact 🖤";
        return "Critical Industrial Impact 💀";
      })();

      valueDiv.appendChild(mainValue);
      valueDiv.appendChild(subValue);
      valueDiv.appendChild(statusText);

      totalBox.appendChild(labelDiv);
      totalBox.appendChild(valueDiv);
      printContainer.appendChild(totalBox);

      // Clone and add all other sections (excluding the original total box and export button)
      const sections = element.querySelectorAll(
        ".summary-section, .equivalency-section, .informational-messages-section"
      );
      sections.forEach((section) => {
        const clonedSection = section.cloneNode(true);
        // Remove any export buttons from cloned sections
        const buttons = clonedSection.querySelectorAll(
          ".export-pdf-button, .export-button"
        );
        buttons.forEach((btn) => btn.remove());
        printContainer.appendChild(clonedSection);
      });

      // Add to DOM temporarily
      document.body.appendChild(printContainer);

      console.log("Print container created, capturing...");

      // Capture the print container
      const canvas = await html2canvas(printContainer, {
        scale: 1.5,
        useCORS: true,
        allowTaint: true,
        backgroundColor: "#ffffff",
        logging: false,
        removeContainer: false,
      });

      // Remove print container
      document.body.removeChild(printContainer);

      // Show export button again
      if (exportButton) {
        exportButton.style.display = "";
      }

      console.log(
        "Canvas created, dimensions:",
        canvas.width,
        "x",
        canvas.height
      );

      // Check if canvas has content
      if (canvas.width === 0 || canvas.height === 0) {
        console.error("Canvas is empty");
        alert("Failed to capture content. Please try again.");
        return;
      }

      // Create PDF
      const imgData = canvas.toDataURL("image/png");
      console.log("Image data created, length:", imgData.length);

      const pdf = new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "a4",
      });

      // Calculate dimensions
      const pdfWidth = 210;
      const pdfHeight = 297;
      const canvasAspectRatio = canvas.height / canvas.width;
      const pdfContentWidth = pdfWidth - 20;
      const pdfContentHeight = pdfContentWidth * canvasAspectRatio;

      console.log(
        "PDF dimensions calculated:",
        pdfContentWidth,
        "x",
        pdfContentHeight
      );

      // Add image to PDF
      if (pdfContentHeight <= pdfHeight - 20) {
        pdf.addImage(imgData, "PNG", 10, 10, pdfContentWidth, pdfContentHeight);
      } else {
        // Split across multiple pages
        const pageContentHeight = pdfHeight - 20;
        const totalPages = Math.ceil(pdfContentHeight / pageContentHeight);

        for (let i = 0; i < totalPages; i++) {
          if (i > 0) pdf.addPage();

          const sourceY =
            (i * pageContentHeight * canvas.height) / pdfContentHeight;
          const sourceHeight = Math.min(
            (pageContentHeight * canvas.height) / pdfContentHeight,
            canvas.height - sourceY
          );

          const pageCanvas = document.createElement("canvas");
          pageCanvas.width = canvas.width;
          pageCanvas.height = sourceHeight;
          const pageCtx = pageCanvas.getContext("2d");

          pageCtx.drawImage(
            canvas,
            0,
            sourceY,
            canvas.width,
            sourceHeight,
            0,
            0,
            canvas.width,
            sourceHeight
          );

          const pageImgData = pageCanvas.toDataURL("image/png");
          const pageHeight = (sourceHeight * pdfContentWidth) / canvas.width;

          pdf.addImage(pageImgData, "PNG", 10, 10, pdfContentWidth, pageHeight);
        }
      }

      // Generate filename
      const timestamp = new Date()
        .toISOString()
        .slice(0, 19)
        .replace(/:/g, "-");
      const supplierName =
        supplierData?.Supplier_and_Container?.split(" - ")[0] || "Unknown";
      const filename = `GHG_Emission_Report_${supplierName}_${timestamp}.pdf`;

      console.log("Saving PDF as:", filename);

      // Save the PDF
      pdf.save(filename);

      console.log("PDF export completed successfully");
    } catch (error) {
      console.error("Error generating PDF:", error);

      // Restore export button if hidden
      const exportButton = document.querySelector(".export-pdf-button");
      if (exportButton) {
        exportButton.style.display = "";
      }

      alert(`Failed to generate PDF: ${error.message}. Please try again.`);
    }
  };

  return (
    <div className="emission-summary-container">
      {/* Header with Logo */}
      <div className="summary-header">
        <img
          src="/saxcologo.jpeg"
          alt="Saxco International"
          className="summary-logo"
        />
        <button
          className="export-pdf-button"
          onClick={exportToPDF}
          title="Export report to PDF"
        >
          📄 Export Report
        </button>
      </div>

      {/* Total Emissions Box */}
      <div
        className="total-emissions-box"
        style={{
          backgroundColor: (() => {
            if (totals.totalEmissions === 0) return "#4caf50"; // Bright green for zero emissions (startup)
            // Color progression for industrial scale
            if (totals.totalEmissions <= 1000) return "#fff9c4"; // Light yellow for 1-1000 tonnes
            if (totals.totalEmissions <= 2000) return "#9e9e9e"; // Light grey for 1001-2000
            if (totals.totalEmissions <= 3000) return "#757575"; // Medium grey for 2001-3000
            if (totals.totalEmissions <= 4000) return "#616161"; // Darker grey for 3001-4000
            if (totals.totalEmissions <= 5000) return "#424242"; // Very dark grey for 4001-5000
            return "#303030"; // Almost black for 5000+ tonnes
          })(),
          boxShadow: (() => {
            if (totals.totalEmissions === 0)
              return "0 4px 12px rgba(76, 175, 80, 0.3)";
            if (totals.totalEmissions <= 1000)
              return "0 4px 12px rgba(255, 249, 196, 0.5)";
            return "0 4px 12px rgba(66, 66, 66, 0.3)";
          })(),
          border: (() => {
            if (totals.totalEmissions === 0) return "2px solid #66bb6a";
            if (totals.totalEmissions <= 1000) return "2px solid #f9a825";
            return "2px solid #757575";
          })(),
        }}
      >
        <div
          className="total-emissions-label"
          style={{
            borderRight: (() => {
              if (totals.totalEmissions === 0) return "2px solid #66bb6a";
              if (totals.totalEmissions <= 1000) return "2px solid #f9a825";
              return "2px solid #757575";
            })(),
            borderBottom:
              window.innerWidth <= 768
                ? (() => {
                    if (totals.totalEmissions === 0) return "2px solid #66bb6a";
                    if (totals.totalEmissions <= 1000)
                      return "2px solid #f9a825";
                    return "2px solid #757575";
                  })()
                : "none",
            color: (() => {
              if (totals.totalEmissions <= 1000 && totals.totalEmissions > 0)
                return "#333"; // Dark text for light yellow
              return "white"; // White text for dark backgrounds
            })(),
          }}
        >
          🌍 Total GHG Emissions
          <br />
          (metric tonnes
          <br />
          CO₂e)
        </div>
        <div className="total-emissions-value">
          <div
            style={{
              fontSize: "28px",
              fontWeight: "bold",
              marginBottom: "5px",
              color: (() => {
                if (totals.totalEmissions <= 1000 && totals.totalEmissions > 0)
                  return "#333"; // Dark text for light yellow
                return "white"; // White text for dark backgrounds
              })(),
            }}
          >
            {totals.totalEmissions.toFixed(2)}
          </div>
          <div
            style={{
              fontSize: "14px",
              opacity: "0.9",
              color: (() => {
                if (totals.totalEmissions <= 1000 && totals.totalEmissions > 0)
                  return "#333"; // Dark text for light yellow
                return "white"; // White text for dark backgrounds
              })(),
            }}
          >
            metric tonnes CO₂e
          </div>
          <div
            style={{
              fontSize: "12px",
              marginTop: "5px",
              opacity: "0.8",
              color: (() => {
                if (totals.totalEmissions <= 1000 && totals.totalEmissions > 0)
                  return "#333"; // Dark text for light yellow
                return "white"; // White text for dark backgrounds
              })(),
            }}
          >
            {(() => {
              if (totals.totalEmissions === 0)
                return "No Emissions Calculated 🌱";
              if (totals.totalEmissions <= 1000)
                return "Good Industrial Performance 🌿";
              if (totals.totalEmissions <= 2000)
                return "Moderate Industrial Impact 🔲";
              if (totals.totalEmissions <= 3000)
                return "High Industrial Impact ⬛";
              if (totals.totalEmissions <= 4000)
                return "Very High Industrial Impact 🖤";
              return "Critical Industrial Impact 💀";
            })()}
          </div>
        </div>
      </div>

      {/* Summary: Emissions from Manufacturing */}
      <div className="summary-section">
        <h2>Summary: Emissions from Manufacturing</h2>
        <table className="summary-table">
          <thead>
            <tr>
              <th>Total Material Weight (g)</th>
              <th>Total Material Weight (t)</th>
              <th>Supplier's Emissions Factor (tCO2e)</th>
              <th>Total Emissions (tCO2)</th>
              <th>Total Emissions (metric tonnes CO2)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                {(
                  (emissionResults?.manufacturing_details?.container_weight ||
                    0) *
                  (emissionResults?.manufacturing_details
                    ?.number_of_containers || 0)
                ).toLocaleString()}
              </td>
              <td>{(totals.totalMaterialWeight * 1.10231).toFixed(4)}</td>
              <td>{totals.supplierEmissionFactor}</td>
              <td>{totals.totalManufacturingEmissions.toFixed(2)}</td>
              <td>
                {(
                  emissionResults?.manufacturing_details
                    ?.manufacturing_emissions_metric_tonnes || 0
                ).toFixed(2)}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Summary: Emissions by Fuel or Distance */}
      <div className="summary-section">
        <h2>Summary: Emissions by Fuel or Distance</h2>
        <table className="summary-table">
          <thead>
            <tr>
              <th>Calculation Method</th>
              <th>Greenhouse gas</th>
              <th>Fossil Fuel Emissions (Metric tonnes)</th>
              <th>Biofuel CO2 Emission (metric tonnes)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td rowSpan="3">Fuel</td>
              <td>CO2</td>
              <td>{transportEmissions.fuel.co2.toFixed(3)}</td>
              <td>{transportEmissions.fuel.biofuel.toFixed(3)}</td>
            </tr>
            <tr>
              <td>CH4</td>
              <td>{transportEmissions.fuel.ch4.toFixed(3)}</td>
              <td>0</td>
            </tr>
            <tr>
              <td>N2O</td>
              <td>{transportEmissions.fuel.n2o.toFixed(3)}</td>
              <td>0</td>
            </tr>
            <tr>
              <td rowSpan="3">Distance</td>
              <td>CO2</td>
              <td>{transportEmissions.distance.co2.toFixed(3)}</td>
              <td>{transportEmissions.distance.biofuel.toFixed(3)}</td>
            </tr>
            <tr>
              <td>CH4</td>
              <td>{transportEmissions.distance.ch4.toFixed(3)}</td>
              <td>0</td>
            </tr>
            <tr>
              <td>N2O</td>
              <td>{transportEmissions.distance.n2o.toFixed(3)}</td>
              <td>0</td>
            </tr>
            <tr className="total-row">
              <td colSpan="2">
                <strong>Total (metric tonnes CO2e)</strong>
              </td>
              <td>
                <strong>{totals.totalTransportEmissions.toFixed(3)}</strong>
              </td>
              <td>
                <strong>
                  {(
                    transportEmissions.fuel.biofuel +
                    transportEmissions.distance.biofuel
                  ).toFixed(3)}
                </strong>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Summary: Emissions by Mode of Transport */}
      <div className="summary-section">
        <h2>Summary: Emissions by Mode of Transport</h2>
        <table className="summary-table">
          <thead>
            <tr>
              <th>Mode of Transport</th>
              <th>Scope</th>
              <th colSpan="3">Fossil Fuel Emissions</th>
              <th>Biofuel CO2 Emission (metric tonnes)</th>
            </tr>
            <tr>
              <th></th>
              <th></th>
              <th>Fossil Fuel CO2 (metric tonnes)</th>
              <th>CH4 (kilograms)</th>
              <th>N2O (kilograms)</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Road</td>
              <td>Scope 3</td>
              <td>{transportEmissions.byMode.road.co2.toFixed(3)}</td>
              <td>{(transportEmissions.byMode.road.ch4 * 1000).toFixed(3)}</td>
              <td>{(transportEmissions.byMode.road.n2o * 1000).toFixed(3)}</td>
              <td>{transportEmissions.byMode.road.biofuel.toFixed(3)}</td>
            </tr>
            <tr>
              <td>Rail</td>
              <td>Scope 3</td>
              <td>{transportEmissions.byMode.rail.co2.toFixed(3)}</td>
              <td>{(transportEmissions.byMode.rail.ch4 * 1000).toFixed(3)}</td>
              <td>{(transportEmissions.byMode.rail.n2o * 1000).toFixed(3)}</td>
              <td>{transportEmissions.byMode.rail.biofuel.toFixed(3)}</td>
            </tr>
            <tr>
              <td>Water</td>
              <td>Scope 3</td>
              <td>{transportEmissions.byMode.water.co2.toFixed(3)}</td>
              <td>{(transportEmissions.byMode.water.ch4 * 1000).toFixed(3)}</td>
              <td>{(transportEmissions.byMode.water.n2o * 1000).toFixed(3)}</td>
              <td>{transportEmissions.byMode.water.biofuel.toFixed(3)}</td>
            </tr>
            <tr className="total-row">
              <td colSpan="2">
                <strong>Total Emissions</strong>
              </td>
              <td>
                <strong>
                  {(
                    transportEmissions.byMode.road.co2 +
                    transportEmissions.byMode.rail.co2 +
                    transportEmissions.byMode.water.co2
                  ).toFixed(3)}
                </strong>
              </td>
              <td>
                <strong>
                  {(
                    (transportEmissions.byMode.road.ch4 +
                      transportEmissions.byMode.rail.ch4 +
                      transportEmissions.byMode.water.ch4) *
                    1000
                  ).toFixed(3)}
                </strong>
              </td>
              <td>
                <strong>
                  {(
                    (transportEmissions.byMode.road.n2o +
                      transportEmissions.byMode.rail.n2o +
                      transportEmissions.byMode.water.n2o) *
                    1000
                  ).toFixed(3)}
                </strong>
              </td>
              <td>
                <strong>
                  {(
                    transportEmissions.byMode.road.biofuel +
                    transportEmissions.byMode.rail.biofuel +
                    transportEmissions.byMode.water.biofuel
                  ).toFixed(3)}
                </strong>
              </td>
            </tr>
            <tr className="total-ghg-row">
              <td colSpan="5">
                <strong>Total GHG Emission (metric tonnes CO2e)</strong>
              </td>
              <td>
                <strong>{totals.totalTransportEmissions.toFixed(3)}</strong>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Equivalency Statements */}
      <div className="equivalency-section">
        <table className="equivalency-table">
          <thead>
            <tr>
              <th>Metric Tonnes CO2:</th>
              <th>{totals.totalEmissions.toFixed(2)}</th>
              <th>Equivalency Statement:</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>CO2 per Mile</td>
              <td>2482</td>
              <td>
                {totals.totalEmissions.toFixed(2)} metric tonnes of CO2e is
                equivalent to emissions from{" "}
                {(totals.totalEmissions * 2482).toFixed(0)} miles driven by an
                average gas-powered passenger vehicle
              </td>
            </tr>
            <tr>
              <td>CO2 per Gallon</td>
              <td>113</td>
              <td>
                {totals.totalEmissions.toFixed(2)} metric tonnes of CO2e is
                equivalent to CO2 emissions from{" "}
                {(totals.totalEmissions * 113).toFixed(0)} gallons of gas
                consumed
              </td>
            </tr>
            <tr>
              <td>Recycling Factor</td>
              <td>43.3</td>
              <td>
                {totals.totalEmissions.toFixed(2)} metric tonnes of CO2e is
                equivalent to greenhouse gas emissions avoided by{" "}
                {(totals.totalEmissions * 43.3).toFixed(1)} trash bags of waste
                recycled instead of landfilled
              </td>
            </tr>
            <tr>
              <td>Wind Power Factor</td>
              <td>0.0003</td>
              <td>
                {totals.totalEmissions.toFixed(2)} metric tonnes of CO2e is
                equivalent to greenhouse gas emissions avoided by{" "}
                {(totals.totalEmissions * 0.0003).toFixed(4)} wind turbines
                running for a year
              </td>
            </tr>
            <tr>
              <td>Tree Seedling Factor</td>
              <td>16.5</td>
              <td>
                {totals.totalEmissions.toFixed(2)} metric tonnes of CO2e is
                equivalent to carbon sequestered by{" "}
                {(totals.totalEmissions * 16.5).toFixed(1)} tree seedlings grown
                for 10 years
              </td>
            </tr>
            <tr>
              <td>Forest Factor</td>
              <td>1.2</td>
              <td>
                {totals.totalEmissions.toFixed(2)} metric tonnes of CO2e is
                equivalent to carbon sequestered by{" "}
                {(totals.totalEmissions * 1.2).toFixed(1)} acres of US forests
                in one year
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Informational Messages Section */}
      {informationalMessages.length > 0 && (
        <div className="informational-messages-section">
          <h2>Important Information</h2>
          <div className="messages-container">
            {informationalMessages.map((messageObj, index) => (
              <div key={index} className="info-message">
                <div className="info-icon">ℹ️</div>
                <div className="info-text">
                  {typeof messageObj === "string"
                    ? messageObj
                    : messageObj.message}
                  {messageObj.row && (
                    <span className="row-indicator">
                      {" "}
                      (Row {messageObj.row})
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default EmissionSummary;
