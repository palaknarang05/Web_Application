import React from "react";
import { Bar } from "react-chartjs-2";

function BarChart({ data }) {
  if (!data || Object.keys(data).length === 0) return <p>No data to display</p>;

  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        label: "Count",
        data: Object.values(data),
        backgroundColor: "rgba(54, 162, 235, 0.6)",
      },
    ],
  };

  const options = { responsive: true, maintainAspectRatio: false };

  return <Bar data={chartData} options={options} />;
}

export default BarChart;