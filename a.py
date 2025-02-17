from fastapi import FastAPI, UploadFile, File, Form
from starlette.responses import JSONResponse
import aiofiles
import os
from fastapi.middleware.cors import CORSMiddleware
import logging, json
import pandas as pd 
from pydantic import BaseModel
import numpy as np


logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

# Allow requests from any origin (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to a specific domain in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)
class SparseCSVChunk(BaseModel):
    chunk_number: int
    total_chunks: int
    file_id: str
    csv_data: dict

@app.post("/upload/")
async def upload_sparse_chunk(data: SparseCSVChunk):
    try:
        logging.info(f"Received chunk {data.chunk_number}/{data.total_chunks} for file {data.file_id}")
        num_rows = max(map(int, data.csv_data.keys())) + 1  # Convert string keys to int
        num_cols = max(
            [max(map(int, cols.keys())) for cols in data.csv_data.values()]
        ) + 1  # Convert column keys to int
        sparse_matrix = np.zeros((num_rows, num_cols))
        for row_idx, cols in data.csv_data.items():
            for col_idx, value in cols.items():
                sparse_matrix[int(row_idx), int(col_idx)] = value  # Convert indices to int
        row_sums = np.sum(sparse_matrix, axis=1)
        row_sums = np.nan_to_num(row_sums, nan=0.0, posinf=0.0, neginf=0.0) row_sums_sparse = {str(i): row_sum for i, row_sum in enumerate(row_sums) if row_sum != 0}
        return JSONResponse(content={
            "message": f"Chunk {data.chunk_number}/{data.total_chunks} processed successfully for file {data.file_id}",
            "row_sums": row_sums_sparse
        })

    except Exception as e:
        logging.error(f"Error processing chunk: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)


