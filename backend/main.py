from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve frontend files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

@app.get("/download")
def download_file():
    return FileResponse("installers/installer.zip", filename="installer.zip")

