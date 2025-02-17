async function uploadSparseCsv(file) {
    const reader = new FileReader();

    reader.onload = async function (event) {
        const text = event.target.result;
        const rows = text.split('\n'); // Split CSV by rows
        if( rows.length < 2 ){
            console.warn("CSV file too small");
            return;
        }
        const fileName = file.name;
        const header = rows.shift().(",").slice(1);
        const chunkSize = 100; // Adjust as needed
        const totalChunks = Math.ceil(rows.length / chunkSize);

        const convertToSparse = (chunk) => {
            let sparseChunk = {};
            const rowNames =[];
            chunk.forEach((row, rowIndex) => {
                const values = row.split(','); // Split by comma to get columns
                const rowName = cells.shift();
                rowNames.push(rowName)
                sparseChunk[rowIndex] = {};
                values.forEach((value, colIndex) => {
                    if (value !== '0' && value.trim() !== '') { // Filter out empty and zero values
                        sparseChunk[rowIndex][colIndex] = parseFloat(value);
                    }
                });
            });
            return Object.keys(sparseChunk).length > 0 ? sparseChunk : null;
        };
        
        
        for (let i = 0; i < totalChunks; i++) {
            const start = i * chunkSize;
            const end = start + chunkSize;
            const chunkRows = rows.slice(start, end);
            const sparseChunk = convertToSparse(chunkRows);
            await sendChunk(fileName, sparseChunk, i, totalChunks);
        }

        alert("File upload complete!");
    };

    // Read the file as text
    reader.readAsText(file);
}

// Function to send a chunk to the FastAPI server
async function sendChunk(fileName, sparseChunk, chunkNumber, totalChunks) {
    if (!sparseChunk || Object.keys(sparseChunk).length === 0){
        console.warn(`Skipping empty chunk ${chunkNumber}/${totalChunks}`);
        return;
    }
    const payload = {
        chunk_number: chunkNumber,
        total_chunks: totalChunks,
        file_id: fileName,
        csv_data: sparseChunk // Send as actual JSON, not a string
    };

    try {
        const response = await fetch("http://localhost:8000/upload/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });
        if(!response.ok){
               const errorText = await response.text();
               throw new Error(`Server error: ${errorText}`);
        }
        const result = await response.json();
        console.log("Row sums received:", result);
    } catch (error) {
        console.error("Error uploading chunk:", error);
    }
}
