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
      
      if (error) {
        console.error("Python stderr error:", error);
        reject(error);
        return;
      }
      try {
        const result = JSON.parse(data);
        console.log("Parsed Python result:", result);

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
