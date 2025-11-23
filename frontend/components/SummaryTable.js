import React from "react";

function SummaryTable({ summary }) {
  return (
    <div className="summary-table">
      <h2>Summary Statistics</h2>
      <table>
        <tbody>
          <tr><td>Total Equipment</td><td>{summary.total_equipment}</td></tr>
          <tr><td>Average Flowrate</td><td>{summary.average_flowrate.toFixed(2)}</td></tr>
          <tr><td>Average Pressure</td><td>{summary.average_pressure.toFixed(2)}</td></tr>
          <tr><td>Average Temperature</td><td>{summary.average_temperature.toFixed(2)}</td></tr>
        </tbody>
      </table>
    </div>
  );
}

export default SummaryTable;