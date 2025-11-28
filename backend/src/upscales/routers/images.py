from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
import subprocess
from PIL import UnidentifiedImageError, Image
import uuid
import asyncio
from pathlib import Path
import shutil

router = APIRouter(
    tags=["images"],
    prefix="/images"
)

Input_Folder = Path("./backend/src/ESRGAN/LR/")
Output_Folder = Path("./Upscaled-Images")
Input_Folder.mkdir(exist_ok=True, parents=True)
Output_Folder.mkdir(exist_ok=True, parents=True)

_FOLDER_LOCK = asyncio.Semaphore(1)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_images(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No files uploaded")

    saved_filenames = []
    failed = []

    async with _FOLDER_LOCK:
        # clear Input_Folder (same behavior as before)
        for item in Input_Folder.iterdir():
            try:
                if item.is_file() or item.is_symlink():
                    item.unlink()
                else:
                    shutil.rmtree(item)
            except Exception:
                pass

        # validate & save each uploaded image into INPUT folder (not OUTPUT)
        for upload in files:
            try:
                # ensure file pointer is at start (defensive)
                try:
                    upload.file.seek(0)
                except Exception:
                    pass

                # use context manager and force load to detect corrupt images early
                with Image.open(upload.file) as img:
                    img.load()
                    fmt = (img.format or "PNG").lower()
                    # normalize jpeg -> jpg
                    if fmt == "jpeg":
                        ext = "jpg"
                    else:
                        ext = fmt
                    server_side_name = f"{uuid.uuid4().hex}.{ext}"
                    destination_path = Input_Folder / server_side_name
                    img.save(destination_path)
                    saved_filenames.append(server_side_name)

            except UnidentifiedImageError:
                failed.append(upload.filename)
            except Exception as e:
                # record failure but continue with other files
                failed.append(upload.filename)
                # optionally log e

        # if nothing valid, cleanup and return error (no upscaler started)
        if not saved_filenames:
            shutil.rmtree(Input_Folder, ignore_errors=True)
            Input_Folder.mkdir(parents=True, exist_ok=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No valid images uploaded; failed: {failed}")

        # start the upscaler (non-blocking) - unchanged command
        subprocess.Popen([
            "./backend/venv/Scripts/python.exe",
            "./backend/src/ESRGAN/test.py"
        ])

    return {"saved": saved_filenames, "failed": failed}
