import React, { useState } from "react";
import axios from "axios";
import ShowData from "./ShowData";

const UploadFile = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showImageChart, setShowImageChart] = useState(false);
  const [chartUrl, setChartUrl] = useState("");

  const uploadFile = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    setLoading(true);
    setMessage("📊 Analyzing your file...");
    setChartData(null);
    setChartUrl("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:5000/api/upload",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      console.log("Backend Response:", response.data);
      setMessage("✅ File processed successfully!");
      const data = response.data;

      if (data.chartData && data.chartData.labels && data.chartData.datasets) {
        setChartData({
          labels: data.chartData.labels,
          datasets: data.chartData.datasets.map((dataset) => ({
            ...dataset,
            tension: 0.1,
            pointRadius: 2,
            pointHoverRadius: 5,
          })),
        });
        setShowImageChart(false);
      } else if (data.chartUrl) {
        setChartUrl(data.chartUrl + `?t=${Date.now()}`);
        setShowImageChart(true);
      } else {
        setMessage("Analysis completed but no chart data received.");
      }
    } catch (error) {
      console.error("Upload Error:", error);
      setMessage("❌ Failed to upload file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center text-center bg-gray-50 border p-5 rounded-lg shadow-md max-w-6xl mx-auto my-3">
      <h1 className="font-bold text-3xl mb-4 text-gray-800">
        Stock Analysis Tool
      </h1>
      <p className="text-gray-600 mb-6">
        Upload your stock data (CSV/Excel) for technical analysis
      </p>

      {/* File input */}
      <label className="w-64 m-4 px-4 py-3 bg-blue-700 text-white rounded-lg cursor-pointer hover:bg-blue-600 font-medium">
        <input
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={(e) => setFile(e.target.files[0])}
          className="hidden"
        />
        📁 Choose File
      </label>

      {/* Show selected file */}
      {file && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mt-2">
          <p className="text-sm text-blue-800">
            📂 Selected: <span className="font-semibold">{file.name}</span>
          </p>
          <p className="text-xs text-blue-600 mt-1">
            Size: {(file.size / 1024).toFixed(1)} KB
          </p>
        </div>
      )}

      {/* Upload button */}
      <button
        className={`block w-80 py-3 px-4 rounded-lg mt-4 font-medium ${
          loading
            ? "bg-gray-400 text-gray-700 cursor-not-allowed"
            : "bg-green-600 text-white hover:bg-green-700 cursor-pointer"
        }`}
        onClick={uploadFile}
        disabled={loading || !file}
      >
        {loading ? "🔄 Processing..." : "🚀 Upload & Analyze"}
      </button>

      {/* Status message */}
      {message && (
        <div
          className={`mt-5 p-3 rounded-lg font-medium ${
            message.includes("✅")
              ? "bg-green-100 text-green-800 border border-green-200"
              : message.includes("❌")
              ? "bg-red-100 text-red-800 border border-red-200"
              : "bg-blue-100 text-blue-800 border border-blue-200"
          }`}
        >
          {message}
        </div>
      )}

      {/* Chart component */}
      <ShowData
        chartData={chartData}
        showImageChart={showImageChart}
        chartUrl={chartUrl}
      />

      {/* Instructions */}
      {!file && (
        <div className="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-4 max-w-2xl">
          <h3 className="font-semibold text-yellow-800 mb-2">
            📋 File Requirements:
          </h3>
          <ul className="text-sm text-yellow-700 text-left space-y-1">
            <li>• CSV or Excel format (.csv, .xlsx, .xls)</li>
            <li>• Must contain 'Date' and 'Avg' columns</li>
            <li>• Date should be in standard format (YYYY-MM-DD)</li>
            <li>• Avg should contain numeric price values</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default UploadFile;
