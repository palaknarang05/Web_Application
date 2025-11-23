import React, { useState } from "react";

function CSVUploader({ setSummaryData, setHistory }) {
  const [fileName, setFileName] = useState("No file selected");

  const handleFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:8000/api/equipment/", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    setSummaryData(data.summary);
    setHistory(data.history);
  };

  return (
    <div className="csv-uploader">
      <input type="file" accept=".csv" onChange={handleFile} />
      <p>Selected: {fileName}</p>
    </div>
  );
}

export default CSVUploader;