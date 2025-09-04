import express from "express";
import cors from "cors";
import uploadRoutes from "./routes/uploadRoutes.js";

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());

app.use(
  cors({
    origin: process.env.FRONTEND_URL || "*",

    methods: ["GET", "POST"],
    credentials: true,
  })
);

// serve static files from uploads folder
app.use("/uploads", express.static("uploads"));

// serve static files from /tmp for production
if (process.env.RENDER) {
  app.use("/uploads", express.static("/tmp"));
}

// health check route
app.get("/", (req, res) => {
  res.json({
    message: "Stock Analysis API is running!",
    status: "healthy",
    endpoints: {
      upload: "/api/upload"
    }
  });
});

// routes
app.use("/api/upload", uploadRoutes);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
