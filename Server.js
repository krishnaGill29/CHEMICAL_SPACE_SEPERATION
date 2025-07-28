const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

// Serve static HTML
app.use(express.static(path.join(__dirname, 'public')));

// Endpoint to trigger the prediction script
app.get('/run-prediction', async (req, res) => {
    const { exec } = require('child_process');
    exec('node process_predict.js', (err, stdout, stderr) => {
        if (err) {
            console.error("Script error:", stderr);
            return res.status(500).send("Prediction script failed.");
        }
        res.send("Prediction completed successfully.");
    });
});

// Endpoint to serve generated CSV
app.get('/get-predictions', (req, res) => {
    const filePath = path.join(__dirname, 'files', 'activity_predictions.csv');
    fs.access(filePath, fs.constants.F_OK, (err) => {
        if (err) {
            return res.status(404).send("File not found.");
        }
        res.sendFile(filePath);
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
