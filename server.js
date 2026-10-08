require("dotenv").config();

const express = require("express");
const cors = require("cors");

const authRoutes = require("./routes/auth");
const workerRoutes = require("./routes/worker");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/worker", workerRoutes);

// Home / health check
app.get("/", (req, res) => {
  res.json({
    status: "Online",
    system: "SIH 2026 Core Backend & Auth API Server",
  });
});

// Start server
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`SIH Core Backend running on http://localhost:${PORT}`);
});
