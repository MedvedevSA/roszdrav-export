from typing import List
from pathlib import Path
from os import walk
from os.path import getctime

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, Body
from uploads_parser import Parser

data_path = Path('./.data')
parser = Parser()

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    current_file = (await files())[0]

    parser.set_file_path(current_file)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/raw_data")
async def root():
    return parser.parse()


@app.post("/upload_file/")
async def upload_file(files: List[UploadFile]):
    for file in files:
        contents = await file.read()
        path_to_save = data_path / file.filename

        with open(path_to_save, 'wb') as write_file:
            write_file.write(contents)
        parser.set_file_path(file.filename)

    return {"filenames": [file.filename for file in files]}


@app.get("/files/")
async def files():
    file_names = [filenames for _, _, filenames in walk(data_path)]
    file_names = file_names[0] if file_names else []

    file_names.sort(key=lambda file: getctime(data_path / file), reverse=True)
    return file_names


@app.get("/current_file/")
async def get_current_file() -> str:
    return  parser.file_path


@app.post("/set_file/")
async def set_file(file_name: str = Body()):
    parser.set_file_path(file_name)
    return 


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8000,
        log_level='debug',
        access_log=True,
        reload=True
    )
