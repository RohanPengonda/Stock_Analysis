// routes/uploadRoutes.js
import express from "express";
import upload from "../middleware/upload.js";
import { handleUpload } from "../controllers/uploadControllers.js";

const router = express.Router();

router.post("/", upload.single("file"), handleUpload);

export default router;
