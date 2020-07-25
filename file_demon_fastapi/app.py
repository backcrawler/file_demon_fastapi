from fastapi import FastAPI, File, Response, UploadFile
import aiofiles.os as aios
from aiofiles import open

import os

from .utils import get_hash_name, find_correct_dir
from .settings import STORAGE_DIRNAME

app = FastAPI()
upload_dir = os.path.join(os.getcwd(), STORAGE_DIRNAME)


@app.get("/api/{hash_name}/")
async def download_file(hash_name: str):
    pathname = os.path.join(upload_dir, find_correct_dir(hash_name))
    try:
        async with open(pathname, 'rb') as f:
            file_obj = await f.read()
    except FileNotFoundError:
        return Response(status_code=404)
    return {"file": file_obj}


@app.post("/api/")
async def upload_file(file: bytes = File(...)):
    hash_name = get_hash_name(file)
    pathname = os.path.join(upload_dir, find_correct_dir(hash_name))
    if not os.path.exists(pathname):
        if not os.path.exists(os.path.dirname(pathname)):
            await aios.mkdir(os.path.dirname(pathname))
        async with open(pathname, 'wb') as f:
            await f.write(file)
    return {"name": hash_name}


@app.delete("/api/{hash_name}/")
async def remove_file(hash_name: str):
    filepath = os.path.join(upload_dir, find_correct_dir(hash_name))
    try:
        await aios.remove(filepath)
    except FileNotFoundError:
        return Response(status_code=404)
    else:
        return Response(status_code=200)