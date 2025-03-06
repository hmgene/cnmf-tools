const express = require("express");
const path = require("path");

const app = express();
const PORT = 3000;

// Serve frontend
app.use(express.static("frontend"));

// Endpoint to download the app
app.get("/download", (req, res) => {
    const file = path.join(__dirname, "installers", "app-installer.zip");
    res.download(file);
});

app.listen(PORT, () => console.log(`Server running at http://localhost:${PORT}`));
