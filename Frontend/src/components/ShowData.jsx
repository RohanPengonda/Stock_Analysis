import React from "react";
import { Line } from "react-chartjs-2";

const ShowData = ({ chartData, showImageChart, chartUrl }) => {
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: "top" },
      title: {
        display: true,
        text: "Stock Price Analysis with Moving Averages",
        font: { size: 16, weight: "bold" },
      },
    },
    scales: {
      x: { display: true, title: { display: true, text: "Date" } },
      y: { display: true, title: { display: true, text: "Price ($)" } },
    },
    interaction: { mode: "index", intersect: false },
  };

  if (!chartData && !showImageChart) return null;

  return (
    <div className="mt-8 w-full max-w-5xl bg-white rounded-lg shadow-lg p-6">
      {chartData && !showImageChart && (
        <div className="h-96">
          <Line data={chartData} options={chartOptions} />
        </div>
      )}
      {showImageChart && chartUrl && (
        <>
          <h3 className="text-lg font-semibold mb-4 text-gray-800">
            Analysis Chart
          </h3>
          <img
            src={chartUrl}
            alt="Stock Analysis Chart"
            className="w-full h-auto rounded-lg border"
            onError={(e) => console.error("Image failed to load:", chartUrl)}
          />
        </>
      )}
    </div>
  );
};

export default ShowData;
