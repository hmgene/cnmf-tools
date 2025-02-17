# flask_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_chunk():
    file = request.files['file']
    index = int(request.form['index'])
    total_chunks = int(request.form['totalChunks'])
    file_name = request.form['fileName']

    # Save the chunk
    chunk_path = os.path.join(UPLOAD_FOLDER, f"{file_name}.part{index}")
    file.save(chunk_path)

    # If all chunks are uploaded, reassemble the file
    if index == total_chunks - 1:
        reassemble_file(file_name, total_chunks)

    return jsonify({"message": "Chunk uploaded successfully"}), 200

def reassemble_file(file_name, total_chunks):
    # Combine all chunks into a single CSV file
    combined_df = pd.DataFrame()
    for i in range(total_chunks):
        chunk_path = os.path.join(UPLOAD_FOLDER, f"{file_name}.part{i}")
        chunk_df = pd.read_csv(chunk_path)
        combined_df = pd.concat([combined_df, chunk_df])
        os.remove(chunk_path)  # Clean up the chunk after reassembly

    # Save the combined CSV file
    combined_file_path = os.path.join(UPLOAD_FOLDER, file_name)
    combined_df.to_csv(combined_file_path, index=False)

if __name__ == '__main__':
    app.run(port=5000)
