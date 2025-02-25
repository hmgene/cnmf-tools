from fastapi import FastAPI, UploadFile, File, Form
from starlette.responses import JSONResponse
import csv,os, logging, json
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd 
from pydantic import BaseModel
import numpy as np
from pathlib import Path
import src.cnmf

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
    spectra: str
    csv_data: list

@app.get("/get_spectra")
async def get_spectra():
    spectra_files = [f.name for f in Path("data/spectra").glob("*.txt")]
    return {"spectra_files":spectra_files}

@app.post("/upload/")
async def upload_sparse_chunk(data: SparseCSVChunk):
    try:
        logging.info(f"Received chunk {data.chunk_number}/{data.total_chunks} for file {data.file_id}")
        tt=pd.DataFrame(data.csv_data)
        H = pd.read_table(f"data/spectra/{data.spectra}", sep="\t", index_col=0,  encoding="latin1");
        
        json_data = H.to_json(orient="records")
        return JSONResponse(content={
            "message": f"Chunk {data.chunk_number}/{data.total_chunks} processed successfully for file {data.file_id}",
            "data": json_data
        })

    except Exception as e:
        logging.error(f"Error processing chunk: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)


