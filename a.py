import streamlit as st
import json

# Set up the Streamlit app
st.set_page_config(page_title="CSV Uploader", layout="wide")
st.title("CSV Uploader with Button")

# Create a placeholder to display output
output_placeholder = st.empty()

# HTML to embed in the Streamlit app
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Uploader</title>
</head>
<body>
    <h2>Upload CSV</h2>
    <input type="file" id="csvInput" accept=".csv">
    <p id="status">Waiting for file...</p>
    <pre id="output"></pre>  <!-- Output area -->

    <button id="sendButton">Send Data to Streamlit</button>  <!-- Button to trigger send -->

    <script>
        // Handle file input
        document.getElementById("csvInput").addEventListener("change", function(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {

                // Update the <pre id="output"></pre> element with preview text
                document.getElementById("output").textContent = "hi";
                document.getElementById("status").textContent = "File loaded. Ready to send.";
            };

            document.getElementById("status").textContent = "Processing...";
            reader.readAsText(file);
        });

        // Handle button click
        document.getElementById("sendButton").addEventListener("click", function() {
            const outputContent = document.getElementById("output").textContent;
            
            // Send the content of the output <pre> to Streamlit using postMessage
            if (window.parent !== window) {
                window.parent.postMessage({ outputData: outputContent }, "*");
            }
        });
    </script>
</body>
</html>
"""

# Display the HTML code in the Streamlit app
st.components.v1.html(html_code, height=400)

# Listen for messages from JavaScript (via postMessage)
def listen_for_data():
    # Streamlit won't directly expose JavaScript variables, so we use `st.experimental_get_query_params()`
    message = st.experimental_get_query_params()
    if 'outputData' in message:
        return message['outputData'][0]  # Capture the `outputData`
    return None

# Capture the output data (sent via postMessage)
output_data = listen_for_data()

if output_data:
    # Display the processed data in Streamlit
    output_placeholder.text(f"Processed Data:\n{output_data}")

