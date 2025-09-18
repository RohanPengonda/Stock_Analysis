import React, { useState } from "react";
import axios from "axios";

const UploadFile = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [chartUrl, setChartUrl] = useState("");
  const [predictionData, setPredictionData] = useState(null);

  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

  const uploadFile = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      alert("Please select a file first.");
      return;
    }

    setLoading(true);
    setMessage("Analyzing your file...");
    setChartUrl("");
    setPredictionData(null); // Clear previous predictions

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API_URL}/api/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const data = response.data;

      if (data.chartUrl) {
        setChartUrl(data.chartUrl + `?t=${Date.now()}`);

        // Store prediction data
        if (data.hasPredictions) {
          setPredictionData({
            predictions: data.predictions,
            dates: data.predictionDates,
            count: data.predictions.length,
          });
          setMessage(
            `Analysis completed with ${data.predictions.length}-day price predictions!`
          );
        } else {
          setPredictionData(null);
          setMessage(
            " Analysis completed! (Need 30+ days of data for predictions)"
          );
        }
      } else {
        setMessage("Analysis completed but no chart data received.");
      }
    } catch (error) {
      setMessage(" Failed to upload file.");
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
          onChange={(e) => {
            setFile(e.target.files[0]);
            setPredictionData(null); // Clear predictions when new file selected
            setChartUrl(""); // Clear previous chart
            setMessage(""); // Clear previous message
          }}
          className="hidden"
        />
        Choose File
      </label>

      {/* Show selected file */}
      {file && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mt-2">
          <p className="text-sm text-blue-800">
            Selected: <span className="font-semibold">{file.name}</span>
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
        disabled={loading}
      >
        {loading ? " Processing..." : " Upload & Analyze"}
      </button>

      {/* Status message */}
      {message && (
        <div
          className={`mt-5 p-3 rounded-lg font-medium ${
            message.includes("Yes...")
              ? "bg-green-100 text-green-800 border border-green-200"
              : message.includes("No.....")
              ? "bg-red-100 text-red-800 border border-red-200"
              : "bg-blue-100 text-blue-800 border border-blue-200"
          }`}
        >
          {message}
        </div>
      )}

      {/* Chart Image */}
      {chartUrl && (
        <div className="mt-8">
          <img
            src={chartUrl}
            alt="Stock Analysis Chart"
            className="max-w-full h-auto rounded-lg shadow-lg"
          />
        </div>
      )}

      {/* Prediction Details */}
      {predictionData && (
        <div className="mt-6 bg-purple-50 border border-purple-200 rounded-lg p-4 max-w-4xl">
          <h3 className="font-semibold text-purple-800 mb-3 text-lg">
            🔮 Price Predictions (Next {predictionData.count} Days)
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {predictionData.predictions.map((price, index) => (
              <div
                key={index}
                className="bg-white rounded-lg p-3 border border-purple-100"
              >
                <div className="text-sm text-purple-600 font-medium">
                  {new Date(predictionData.dates[index]).toLocaleDateString()}
                </div>
                <div className="text-lg font-bold text-purple-800">
                  ${price.toFixed(2)}
                </div>
              </div>
            ))}
          </div>
          <div className="mt-3 text-xs text-purple-600">
            * Predictions based on Linear Regression model using historical
            price patterns and moving averages
          </div>
        </div>
      )}

      {/* Instructions */}
      {!file && (
        <div className="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-4 max-w-2xl">
          <h3 className="font-semibold text-yellow-800 mb-2">
            File Requirements:
          </h3>
          <ul className="text-sm text-yellow-700 text-left space-y-1">
            <li>• CSV or Excel format (.csv, .xlsx, .xls)</li>
            <li>• Must contain 'Date' and 'Avg'/'Close' columns</li>
            <li>• Date should be in standard format (YYYY-MM-DD)</li>
            <li>• Price values should be numeric</li>
            <li>• 30+ days of data recommended for predictions</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default UploadFile;
