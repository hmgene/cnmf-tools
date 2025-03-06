const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

app.post('/endpoint', (req, res) => {
    const chunkData = req.body.data;
    console.log('Received chunk:', chunkData);
    
    // Do some processing and return a response
    res.json({ status: 'success', chunkSize: chunkData.length });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

