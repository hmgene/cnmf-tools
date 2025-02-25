 
function csv2json2serv(file_id, csvString, chunkSize, serverUrl, status_id,spectra) {
    const rows = csvString.trim().split("\n");
    const totalChunks = Math.ceil(rows.length / chunkSize);
    const headers = rows.shift().split(",");
    let result = [];
    if (headers[0] === "") { headers[0] = "id"; }

    function processChunk(i) {
        const chunk = rows.slice(i*chunkSize, i*chunkSize + chunkSize);
        const jsonData = csv2json(headers.join(",") + "\n" + chunk.join("\n"));
        const cn = i+1;

        return fetch(serverUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chunk_number: cn,
                total_chunks: totalChunks,
                file_id: file_id,
                spectra: spectra,
                csv_data: jsonData
            })
        })
        .then(response => response.json())
        .then(res => {
            document.getElementById(status_id).textContent = `Server Response for chunk ${cn} / ${totalChunks}`;
            result.push(...JSON.parse( res.data ) );
        })
        .catch(error => {
            console.error('Error sending chunk to server:', error);
        });
    }

    const chunkPromises = [];
    for (let i = 0; i < totalChunks; i++) {
        chunkPromises.push(processChunk(i));
    }

    return Promise.all(chunkPromises)
        .then(() => result)  // Once all fetches are completed, return the result
        .catch(error => {
            console.error('Error during chunk processing:', error);
            throw error;
        });
}

       function mem() {
            requestAnimationFrame(() => {
                const status = document.getElementById("status");
                
                if (!performance.memory) {
                    status.textContent = "Memory usage reporting is not supported in this browser.";
                    return;
                }

                const { usedJSHeapSize, totalJSHeapSize, jsHeapSizeLimit } = performance.memory;
                console.log(usedJSHeapSize)
                status.textContent = `Current Heap Usage: ${(usedJSHeapSize / 1024 / 1024).toFixed(2)} MB / ${(totalJSHeapSize / 1024 / 1024).toFixed(2)} MB ( Heap Limit: ${(jsHeapSizeLimit / 1024 / 1024).toFixed(2)} MB )
        `;
            });
        }
        function csv2json(csvString) {
            const rows = csvString.trim().split("\n");
            const headers = rows.shift().split(",");
            if( headers[0] === "" ){ headers[0] = "id";}
            return rows.map(row => {
                const values = row.split(",");
                return headers.reduce((acc, header, index) => {
                    if(values[index]) acc[header] = values[index];
                    return acc;
                }, {});
            });
        }

        function json2csv(jsonArray) {
            console.log(jsonArray)
            if (!jsonArray.length) return "";
            const headers = Object.keys(jsonArray[0]).join(",");
            if( headers[0] === "" ){ headers[0] = "id";}
            const rows = jsonArray.map(obj => Object.values(obj).join(",")).join("\n");
            return `${headers}\n${rows}`;
        }

        // Function to trigger CSV file download
        function downloadCsv(filename, csvString) {
            const blob = new Blob([csvString], { type: "text/csv" });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // Convert JSON to CSV and download
        function downloadConvertedCsv() {
            if (!jsonData.length) {
                alert("No JSON data available. Please upload a CSV file first.");
                return;
            }
            const csvString = json2csv(jsonData);
            downloadCsv("converted_output.csv", csvString);
        }
