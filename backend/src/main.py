from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import subprocess
from pathlib import Path
import shutil
from time import sleep

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/process", tags=["image-processing"])
async def upscaleImage(file: UploadFile = File(...)):
    image = Image.open(file.file)
    inputFolder = "./backend/src/ESRGAN/LR"
    image.save(f"{inputFolder}/img.jpeg")

    # delete contents of the input folder beforehand
    folder = Path(inputFolder)
    for item in folder.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
        else:
            shutil.rmtree(item)

    subprocess.run(["./backend/venv/Scripts/python.exe", "./backend/src/ESRGAN/test.py"])

    output_path = "backend/src/ESRGAN/results"
    sleep(5)
    while(True):
        with open("backend/signal.txt") as f:
            signal = f.read()
            if(signal == "1"):
                return FileResponse(f"{output_path}/img_rlt.png", media_type="image/png")
        sleep(1)