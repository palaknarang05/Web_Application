<div style={{ overflowX: "auto", width: "100%" }}>
  <table
    style={{
      width: "100%",
      maxWidth: "600px",
      margin: "20px auto",
      borderCollapse: "separate",
      borderSpacing: 0,
      borderRadius: "12px",
      overflow: "hidden",
      boxShadow: "0 6px 15px rgba(0,0,0,0.1)",
      fontSize: "clamp(14px, 2vw, 16px)",
      backgroundColor: "#ffffff",
      textAlign: "center", // ⬅ Center table content horizontally
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
        <td style={{ padding: "14px", fontWeight: "500", color: "#20c997" }}>
          Avg Flowrate
        </td>
        <td style={{ padding: "14px", fontWeight: "600", color: "#495057" }}>
          {summary.average_flowrate.toFixed(2)}
        </td>
      </tr>
      <tr style={{ backgroundColor: "#e9f2ff" }}>
        <td style={{ padding: "14px", fontWeight: "500", color: "#6610f2" }}>
          Avg Pressure
        </td>
        <td style={{ padding: "14px", fontWeight: "600", color: "#495057" }}>
          {summary.average_pressure.toFixed(2)}
        </td>
      </tr>
      <tr>
        <td style={{ padding: "14px", fontWeight: "500", color: "#ffc107" }}>
          Avg Temperature
        </td>
        <td style={{ padding: "14px", fontWeight: "600", color: "#495057" }}>
          {summary.average_temperature.toFixed(2)}
        </td>
      </tr>
    </tbody>
  </table>
</div>