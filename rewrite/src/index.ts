import express from "express";

import initializeRoutes from "./utils/initializeRoutes";

const app = express();
app.use(express.json());

console.log("[./src/index] Initializing Routes...");
initializeRoutes(app);

console.log("[./src/index] App Listening At http://localhost:3000");
app.listen(3000);