import { spawn } from "child_process";

export const runPythonAnalysis = (filePath) => {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn("python", ["./python/analyze.py", filePath]);

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
      if (error) {
        reject(error);
        return;
      }
      try {
        const result = JSON.parse(data);

        // Add full URL for frontend
        if (result.chartPath) {
          result.chartUrl = `http://localhost:5000/${result.chartPath}`;
        }

        resolve(result);
      } catch (err) {
        reject(`Failed to parse Python output: ${err}`);
      }
    });
  });
};
