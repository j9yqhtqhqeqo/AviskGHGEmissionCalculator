import React from "react";
import "../styles/EmissionSummary.css";
import saxcoLogo from "../assets/saxcologo.jpeg";

function EmissionSummary() {
  return (
    <div className="emission-summary-container">
      {/* Header with Logo */}
      <div className="summary-header">
        <img
          src="/saxcologo.jpeg"
          alt="Saxco International"
          className="summary-logo"
        />
      </div>

      {/* Total Emissions Box */}
      <div className="total-emissions-box">
        <div className="total-emissions-label">
          Total Emissions
          <br />
          (metric tonnes
          <br />
          CO2)
        </div>
        <div className="total-emissions-value">5,620.35</div>
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
              <td>361,800,000</td>
              <td>420.06</td>
              <td>14.4</td>
              <td>6057.28</td>
              <td>5495.04</td>
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
              <td rowSpan="3">Distance</td>
              <td>CO2</td>
              <td>124.931</td>
              <td>0</td>
            </tr>
            <tr>
              <td>CH4</td>
              <td>0.001</td>
              <td>0</td>
            </tr>
            <tr>
              <td>N2O</td>
              <td>0.001</td>
              <td>0</td>
            </tr>
            <tr className="total-row">
              <td colSpan="2">
                <strong>Total (metric tonnes CO2e)</strong>
              </td>
              <td>
                <strong>125.306</strong>
              </td>
              <td>
                <strong>0</strong>
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
              <td>124.931</td>
              <td>1.472</td>
              <td>1.136</td>
              <td>0</td>
            </tr>
            <tr>
              <td>Rail</td>
              <td>Scope 3</td>
              <td>0</td>
              <td>0</td>
              <td>0</td>
              <td>0</td>
            </tr>
            <tr>
              <td>Water</td>
              <td>Scope 3</td>
              <td>0</td>
              <td>0</td>
              <td>0</td>
              <td>0</td>
            </tr>
            <tr className="total-row">
              <td colSpan="2">
                <strong>Total Emissions</strong>
              </td>
              <td>
                <strong>124.931</strong>
              </td>
              <td>
                <strong>1.472</strong>
              </td>
              <td>
                <strong>1.136</strong>
              </td>
              <td>
                <strong>0</strong>
              </td>
            </tr>
            <tr className="total-ghg-row">
              <td colSpan="5">
                <strong>Total GHG Emission (metric tonnes CO2e)</strong>
              </td>
              <td>
                <strong>125.306</strong>
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
              <th>5620.35</th>
              <th>Equivalency Statement:</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>CO2 per Gal</td>
              <td>2.472</td>
              <td>
                5,620.35 metric tonnes of CO2e is equivalent to emissions from
                2,482 miles driven by an average gas-powered passenger vehicle
              </td>
            </tr>
            <tr>
              <td>113</td>
              <td>5,620.35</td>
              <td>
                5,620.35 metric tonnes of CO2e is equivalent to CO2 emissions
                from 113 gallons of gas consumed
              </td>
            </tr>
            <tr>
              <td>43</td>
              <td>5,620.35</td>
              <td>
                5,620.35 metric tonnes of CO2e is equivalent to greenhouse gas
                emissions avoided by 43.3 trash bags of waste recycled instead
                of landfilled
              </td>
            </tr>
            <tr>
              <td>0</td>
              <td>5,620.35</td>
              <td>
                5,620.35 metric tonnes of CO2e is equivalent to greenhouse gas
                emissions avoided by wind turbines running for a year
              </td>
            </tr>
            <tr>
              <td>17</td>
              <td>5,620.35</td>
              <td>
                5,620.35 metric tonnes of CO2e is equivalent to carbon
                sequestered by 16.5 tree seedlings grown for 10 years
              </td>
            </tr>
            <tr>
              <td>1</td>
              <td>5,620.35</td>
              <td>
                5,620.35 metric tonnes of CO2e is equivalent to carbon
                sequestered by 1.2 acres of US forests in one year
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default EmissionSummary;
