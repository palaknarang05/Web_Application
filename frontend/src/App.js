import React, { useState } from "react";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  ArcElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

ChartJS.register(
  CategoryScale,
  LinearScale,
  ArcElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState([]);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a CSV file first!");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/equipment/", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (response.ok) {
        setSummary(data);
        setMessage("File uploaded successfully!");
      } else {
        setMessage(data.error || "Failed to upload file.");
      }
    } catch (error) {
      setMessage("An error occurred while uploading.");
    }
  };

  const handleDownloadPDF = () => {
    const input = document.getElementById("pdf-content");

    html2canvas(input, { scale: 2, useCORS: true, scrollY: -window.scrollY }).then(
      (canvas) => {
        const imgData = canvas.toDataURL("image/png");
        const pdf = new jsPDF("p", "mm", "a4");
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();

        const imgWidth = pageWidth;
        const imgHeight = (canvas.height * pageWidth) / canvas.width;

        let heightLeft = imgHeight;
        let position = 0;

        pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;

        while (heightLeft > 0) {
          position = heightLeft - imgHeight;
          pdf.addPage();
          pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
          heightLeft -= pageHeight;
        }
        pdf.save("report.pdf");
      }
    );
  };

  return (
    <div
      style={{
        width: "95%",
        maxWidth: "900px",
        margin: "0 auto",
        marginTop: "20px",
        background: "white",
        padding: "30px",
        borderRadius: "12px",
        boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
        textAlign: "center",
      }}
    >
      {/* HEADER */}
      <h1
        style={{
          background: "linear-gradient(90deg, #007bff, #6610f2)",
          color: "white",
          padding: "18px",
          borderRadius: "10px",
          fontSize: "clamp(20px, 4vw, 32px)",
          boxShadow: "0 3px 8px rgba(0,0,0,0.15)",
        }}
      >
        Chemical Equipment Parameter Visualizer
      </h1>

      {/* FILE INPUT */}
      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        style={{ marginTop: "20px", fontSize: "clamp(14px, 2vw, 18px)" }}
      />

      <br />

      {/* UPLOAD BUTTON */}
      <button
        onClick={handleUpload}
        style={{
          marginTop: "10px",
          padding: "10px 20px",
          backgroundColor: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          fontSize: "clamp(14px, 2vw, 18px)",
        }}
      >
        Upload CSV
      </button>

      {/* UPLOAD MESSAGE */}
      {message && (
        <p
          style={{
            marginTop: "15px",
            fontSize: "clamp(14px, 2vw, 18px)",
            color: message.includes("successfully") ? "green" : "red",
          }}
        >
          {message}
        </p>
      )}

      {/* REPORT SECTION */}
      {summary && (
        <div id="report-section" style={{ marginTop: "30px" }}>
          {/* PDF Button */}
          <button
            onClick={handleDownloadPDF}
            style={{
              padding: "10px 15px",
              marginBottom: "20px",
              backgroundColor: "#28a745",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "clamp(14px, 2vw, 18px)",
            }}
          >
            Download PDF Report
          </button>

          {/* PDF CONTENT */}
          <div id="pdf-content">
            {/* SUMMARY STATISTICS */}
            <h2
              style={{
                fontSize: "clamp(18px, 3vw, 26px)",
                marginTop: "30px",
                fontWeight: "600",
                color: "#343a40",
              }}
            >
              Summary Statistics
            </h2>

            <div style={{ overflowX: "auto", width: "100%" }}>
              <table
                style={{
                  width: "100%",
                  maxWidth: "500px",
                  margin: "20px auto",
                  borderCollapse: "separate",
                  borderSpacing: 0,
                  borderRadius: "12px",
                  overflow: "hidden",
                  boxShadow: "0 6px 15px rgba(0,0,0,0.1)",
                  fontSize: "clamp(14px, 2vw, 16px)",
                  backgroundColor: "#ffffff",
                  textAlign: "left",
                }}
              >
                <tbody>
                  <tr style={{ backgroundColor: "#e9f2ff" }}>
                    <td style={{ padding: "14px", fontWeight: "500", color: "#007bff" }}>
                      Total Equipment
                    </td>
                    <td style={{ padding: "14px", fontWeight: "600", color: "#495057" }}>
                      {summary.total_equipment}
                    </td>
                  </tr>
                  <tr>
                    <td style={{ padding: "14px", fontWeight: "500", color: "#007bff" }}>
                      Avg Flowrate
                    </td>
                    <td style={{ padding: "14px", fontWeight: "600", color: "#495057" }}>
                      {summary.average_flowrate.toFixed(2)}
                    </td>
                  </tr>
                  <tr style={{ backgroundColor: "#e9f2ff" }}>
                    <td style={{ padding: "14px", fontWeight: "500", color: "#007bff" }}>
                      Avg Pressure
                    </td>
                    <td style={{ padding: "14px", fontWeight: "600", color: "#495057" }}>
                      {summary.average_pressure.toFixed(2)}
                    </td>
                  </tr>
                  <tr>
                    <td style={{ padding: "14px", fontWeight: "500", color: "#007bff" }}>
                      Avg Temperature
                    </td>
                    <td style={{ padding: "14px", fontWeight: "600", color: "#495057" }}>
                      {summary.average_temperature.toFixed(2)}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            {/* --- CHARTS SECTION --- */}
            <div style={{ marginTop: "40px" }}>
              <h2
                style={{
                  fontSize: "clamp(18px, 3vw, 26px)",
                  marginBottom: "20px",
                  fontWeight: "600",
                }}
              >
                Equipment Type Distribution
              </h2>

              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "flex-start",
                  flexWrap: "wrap",
                  gap: "50px",
                  marginTop: "40px",
                  background: "#fafafa",
                  padding: "50px",
                  borderRadius: "12px",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.12)",
                  minHeight: "920px",
                }}
              >
                {/* BAR CHART */}
                <div
                  style={{
                    width: "100%",
                    maxWidth: "700px",
                    height: "590px",
                    background: "white",
                    padding: "20px",
                    borderRadius: "12px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                  }}
                >
                  <h3 style={{ marginBottom: "15px" }}>
                    Equipment Type Distribution (Bar)
                  </h3>
                  <Bar
                    data={{
                      labels: Object.keys(summary.type_distribution),
                      datasets: [
                        {
                          label: "Count",
                          data: Object.values(summary.type_distribution),
                          backgroundColor: [
                            "rgba(0, 123, 255, 0.7)",
                            "rgba(102, 16, 242, 0.7)",
                            "rgba(255, 138, 138, 0.7)",
                            "rgba(32, 201, 152, 0.7)",
                            "rgba(255, 193, 7, 0.7)",
                            "rgba(220, 53, 69, 0.7)",
                          ],
                          borderRadius: 6,
                        },
                      ],
                    }}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: { legend: { display: false } },
                      scales: {
                        x: { ticks: { font: { size: 12 } } },
                        y: { ticks: { font: { size: 12 } } },
                      },
                    }}
                  />
                </div>

                {/* PIE CHART */}
                <div
                  style={{
                    width: "100%",
                    maxWidth: "500px",
                    height: "470px",
                    background: "white",
                    padding: "30px",
                    borderRadius: "12px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                  }}
                >
                  <h3 style={{ marginBottom: "15px" }}>
                    Equipment Type Distribution (Pie)
                  </h3>
                  <div
                    style={{
                      width: "80%",
                      height: "400px",
                      margin: "0 auto",
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                    }}
                  >
                    <Pie
                      data={{
                        labels: Object.keys(summary.type_distribution),
                        datasets: [
                          {
                            data: Object.values(summary.type_distribution),
                            backgroundColor: [
                              "rgba(0, 123, 255, 0.7)",
                              "rgba(102, 16, 242, 0.7)",
                              "rgba(255, 138, 138, 0.7)",
                              "rgba(32, 201, 152, 0.7)",
                              "rgba(255, 193, 7, 0.7)",
                              "rgba(220, 53, 69, 0.7)",
                            ],
                          },
                        ],
                      }}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* HISTORY SECTION */}
            <div style={{ marginTop: "40px" }}>
              <h2>Last 5 Uploads</h2>
              <button
                onClick={async () => {
                  const res = await fetch(
                    "http://127.0.0.1:8000/api/history/"
                  );
                  const data = await res.json();
                  setHistory(data);
                }}
                style={{
                  padding: "8px 14px",
                  backgroundColor: "#6c757d",
                  color: "white",
                  border: "none",
                  borderRadius: "8px",
                  cursor: "pointer",
                  fontSize: "clamp(14px, 2vw, 18px)",
                  transition: "0.3s",
                }}
                onMouseEnter={(e) => (e.target.style.backgroundColor = "#5a6268")}
                onMouseLeave={(e) => (e.target.style.backgroundColor = "#6c757d")}
              >
                Refresh History
              </button>

              <div style={{ width: "100%", overflowX: "auto", marginTop: "20px" }}>
                <table
                  style={{
                    width: "100%",
                    minWidth: "650px",
                    borderCollapse: "separate",
                    borderSpacing: 0,
                    borderRadius: "12px",
                    overflow: "hidden",
                    boxShadow: "0 4px 15px rgba(0,0,0,0.1)",
                    fontSize: "clamp(12px, 1.5vw, 16px)",
                  }}
                >
                  <thead>
                    <tr style={{ backgroundColor: "#f8f9fa" }}>
                      <th style={{ padding: "12px", textAlign: "left" }}>Filename</th>
                      <th style={{ padding: "12px", textAlign: "left" }}>Upload Time</th>
                      <th style={{ padding: "12px", textAlign: "right" }}>Total</th>
                      <th style={{ padding: "12px", textAlign: "right" }}>Flowrate</th>
                      <th style={{ padding: "12px", textAlign: "right" }}>Pressure</th>
                      <th style={{ padding: "12px", textAlign: "right" }}>Temperature</th>
                    </tr>
                  </thead>
                  <tbody>
                    {history.map((item, idx) => (
                      <tr
                        key={idx}
                        style={{
                          backgroundColor: idx % 2 === 0 ? "#fff" : "#f1f3f5",
                          transition: "background-color 0.3s",
                        }}
                        onMouseEnter={(e) =>
                          (e.currentTarget.style.backgroundColor = "#e9ecef")
                        }
                        onMouseLeave={(e) =>
                          (e.currentTarget.style.backgroundColor =
                            idx % 2 === 0 ? "#fff" : "#f1f3f5")
                        }
                      >
                        <td style={{ padding: "10px", whiteSpace: "nowrap" }}>
                          {item.filename}
                        </td>
                        <td style={{ padding: "10px", whiteSpace: "nowrap" }}>
                          {new Date(item.upload_time).toLocaleString()}
                        </td>
                        <td style={{ padding: "10px", textAlign: "right" }}>
                          {item.total_equipment}
                        </td>
                        <td style={{ padding: "10px", textAlign: "right" }}>
                          {item.average_flowrate.toFixed(2)}
                        </td>
                        <td style={{ padding: "10px", textAlign: "right" }}>
                          {item.average_pressure.toFixed(2)}
                        </td>
                        <td style={{ padding: "10px", textAlign: "right" }}>
                          {item.average_temperature.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
