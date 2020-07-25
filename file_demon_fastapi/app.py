from fastapi import FastAPI, File, Response, UploadFile

import os

from .utils import get_hash_name, find_correct_dir
from .settings import STORAGE_DIRNAME

app = FastAPI()
upload_dir = os.path.join(os.getcwd(), STORAGE_DIRNAME)


@app.get("/api/{hash_name}/")
async def download_file(hash_name: str):
    pathname = os.path.join(upload_dir, find_correct_dir(hash_name))
    print('PATH:', pathname)
    try:
        with open(pathname, 'rb') as f:
            file_obj = f.read()
    except FileNotFoundError:
        print('Nothing...')
        return Response(status_code=404)
    return {"file": file_obj}


@app.post("/api/")
async def upload_file(file: bytes = File(...)):
    print('FILE:', file)
    hash_name = get_hash_name(file)
    pathname = os.path.join(upload_dir, find_correct_dir(hash_name))
    print('PATH:', pathname)
    if not os.path.exists(pathname):
        if not os.path.exists(os.path.dirname(pathname)):
            try:
                os.makedirs(os.path.dirname(pathname))
            except OSError as e:  # Guard against race condition
                return Response(status_code=500)
        with open(pathname, 'wb') as f:
            f.write(file)
    return {"name": hash_name}


@app.delete("/api/{hash_name}/")
async def remove_file(hash_name: str):
    filepath = os.path.join(upload_dir, find_correct_dir(hash_name))
    print('PATH:', filepath)
    try:
        os.remove(filepath)
    except FileNotFoundError:
        return Response(status_code=404)
    else:
        return Response(status_code=200)