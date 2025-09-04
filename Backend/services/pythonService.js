import { spawn } from "child_process";

export const runPythonAnalysis = (filePath) => {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn(process.env.PYTHON_CMD || "python", ["./python/analyze.py", filePath]);

    let data = "";
    let error = "";

    // Collect data from Python stdout
    pythonProcess.stdout.on("data", (chunk) => {
      data += chunk.toString();
    });

    // Collect errors from Python stderr
    pythonProcess.stderr.on("data", (chunk) => {
      error += chunk.toString();
    });

    // When Python process finishes
    pythonProcess.on("close", (code) => {
      console.log("Python process exit code:", code);
      console.log("Python stdout:", data);
      console.log("Python stderr:", error);
      
      // Only reject if exit code is non-zero, not just stderr output
      if (code !== 0) {
        console.error("Python process failed with code:", code);
        reject(error || `Python process exited with code ${code}`);
        return;
      }
      try {
        const result = JSON.parse(data);
        console.log("Parsed Python result:", result);

        // Check if Python script returned an error
        if (result.error) {
          console.error("Python script error:", result.error);
          reject(result.error);
          return;
        }

        // Add full URL for frontend
        if (result.chartPath) {
          result.chartUrl = `${process.env.BASE_URL || 'http://localhost:5000'}/${result.chartPath}`;
          console.log("Generated chartUrl:", result.chartUrl);
        } else {
          console.log("No chartPath in result:", result);
        }

        resolve(result);
      } catch (err) {
        console.error("Failed to parse Python output:", err);
        console.error("Raw Python data:", data);
        reject(`Failed to parse Python output: ${err}`);
      }
    });
  });
};
