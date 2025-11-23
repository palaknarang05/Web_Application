import React from "react";
import { Pie } from "react-chartjs-2";

function PieChart({ data }) {
  if (!data || Object.keys(data).length === 0) return <p>No data to display</p>;

  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        data: Object.values(data),
        backgroundColor: [
          "#007bff",
          "#6610f2",
          "#20c997",
          "#ffc107",
          "#dc3545",
          "#fd7e14",
          "#6f42c1",
        ],
      },
    ],
  };

  const options = { responsive: true, maintainAspectRatio: false };

  return <Pie data={chartData} options={options} />;
}

export default PieChart;