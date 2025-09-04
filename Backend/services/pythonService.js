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
      // Only reject if exit code is non-zero, not just stderr output
      if (code !== 0) {
        reject(error || `Python process exited with code ${code}`);
        return;
      }
      try {
        const result = JSON.parse(data);

        // Check if Python script returned an error
        if (result.error) {
          reject(result.error);
          return;
        }

        // Add full URL for frontend
        if (result.chartPath) {
          result.chartUrl = `${process.env.BASE_URL || 'http://localhost:5000'}/${result.chartPath}`;
        }

        resolve(result);
      } catch (err) {
        reject(`Failed to parse Python output: ${err}`);
      }
    });
  });
};
