import path from "path";
import fs from "fs";
import { runPythonAnalysis } from "../services/pythonService.js";

export const handleUpload = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const filePath = path.resolve(req.file.path);  //full path of uploaded file

    const result = await runPythonAnalysis(filePath);  //python analysis

    // Clean up uploaded file after processing
    try {
      fs.unlinkSync(filePath);
    } catch (cleanupError) {
      console.warn("Failed to delete uploaded file:", cleanupError);
    }

    // return data in json 
    res.json({
      message: "Analysis completed",
      chartUrl: result.chartUrl, // image (chart.png)
      dates: result.dates,       // raw data for Chart.js
      avg: result.avg,
      dma50: result.dma50,
      dma100: result.dma100,
      dma200: result.dma200,
    });
  } catch (error) {
    console.error("Upload Controller Error:", error);
    console.error("Error stack:", error.stack);
    
    // Clean up uploaded file even if processing fails
    if (req.file && req.file.path) {
      try {
        fs.unlinkSync(path.resolve(req.file.path));
      } catch (cleanupError) {
        console.warn("Failed to delete uploaded file:", cleanupError);
      }
    }
    res.status(500).json({ 
      error: "Failed to analyze file",
      details: error.message 
    });
  }
};
