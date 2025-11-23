import React, { useEffect } from "react";
import { Bar, Pie } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

function Charts({ summary }) {
  const labels = Object.keys(summary.type_distribution);
  const data = Object.values(summary.type_distribution);

  const barData = {
    labels,
    datasets: [
      {
        label: "Equipment Count",
        data,
        backgroundColor: ["#007bff","#6610f2","#ff8a8a","#20c998","#ffc107","#dc3545"],
      },
    ],
  };

  const pieData = {
    labels,
    datasets: [
      {
        data,
        backgroundColor: ["#007bff","#6610f2","#ff8a8a","#20c998","#ffc107","#dc3545"],
      },
    ],
  };

  return (
    <div className="charts">
      <h2>Equipment Type Distribution</h2>
      <div style={{ display: "flex", justifyContent: "space-around" }}>
        <div style={{ width: "45%" }}><Bar data={barData} /></div>
        <div style={{ width: "45%" }}><Pie data={pieData} /></div>
      </div>
    </div>
  );
}

export default Charts;