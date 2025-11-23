import React from "react";

function HistoryTable({ history }) {
  return (
    <div className="history-table">
      <h2>Last 5 Uploads</h2>
      <table>
        <thead>
          <tr>
            <th>Filename</th>
            <th>Total</th>
            <th>Flowrate</th>
            <th>Pressure</th>
            <th>Temperature</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item, idx) => (
            <tr key={idx}>
              <td>{item.filename}</td>
              <td>{item.total_equipment}</td>
              <td>{item.average_flowrate.toFixed(2)}</td>
              <td>{item.average_pressure.toFixed(2)}</td>
              <td>{item.average_temperature.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HistoryTable;