from apscheduler.schedulers.asyncio import AsyncIOScheduler
import uvicorn

import asyncio

import re
import tkinter as tk
import tkinter.filedialog as fd

from typing import List

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI , HTTPException, Request
from fastapi import File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse


from utils import  import_1c
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Mem ():
    def __init__(self) -> None:
        self.csv_file_name = None
        self.data = import_1c('./uploads/data.xlsx')
        self.el_data = self.gen(self.data)
        self.imported = True
        pass
    def set_gen(self, id):
        for i in range(id):
            self.get_next()

    def reset_gen(self):
        self.el_data = self.gen(self.data)
        return 

    def get_next(self):
        return next(self.el_data)

    def gen(self, data):
        while True:
            for el in data:
                yield el

    def import_xlsx_data(self, file_name):
        self.data = import_1c(file_name)
        self.el_data = self.gen(self.data)
        self.imported = True

    def import_data(self, file_name):
        self.data = import_1c(file_name)
        self.el_data = self.gen(self.data)
        self.imported = True


mem = Mem()

@app.get("/config/", response_class=HTMLResponse)
async def config_page(request: Request):
    #request
    data_dict = mem.data.copy()
    #data_dict = []
    
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            'data_dict' : data_dict,
            'enumirate' : enumerate
        })


@app.post("/setid/")
async def testpost(select: str = Form(...)):

    #(id):(наименование детали)
    pattern = r'(\d{1,3}):([A-Z]{2}[-.0-9A-ZА-Я]{1,})'
    pattern = re.compile(pattern)
    id , name = pattern.findall(select)[0]

    mem.reset_gen()
    mem.set_gen(int(id)-1)

    return {'id':id, "name":name}


@app.post("/updnext/")
async def updnext(select: str = Form(...)):
    print(select)
    return select    


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    
    #with open(file.) as write_file:
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadxlsxdata/")
async def xlsx_upload_files(files: List[UploadFile], response_class=RedirectResponse):
#async def xlsx_upload_files(files: List[bytes] = File(...)):
    for file in files:
        contents = await file.read()
        path_to_save = os.path.join("./uploads", "data.xlsx")

        with open(path_to_save,'wb') as write_file:
            write_file.write(contents)

    mem.import_data(path_to_save)
        
    #return RedirectResponse('https://192.168.1.193:8000/config')
    return {"filenames": [file.filename for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    for file in files:
        contents = await file.read()
        path_to_save = os.path.join("./uploads", file.filename)

        with open(path_to_save,'wb') as write_file:
            write_file.write(contents)
        
    return {"filenames": [file.filename for file in files]}

@app.get("/zdrav")
def zdrav():
    if not mem.imported:
        return HTTPException
    return mem.get_next()

@app.get("/")
def read_root():
    return {"Hello": "World"}



def start_uvicorn():
    uvicorn.run(app, host="0.0.0.0",
                port=8000,
                ssl_keyfile="./key.pem", 
                ssl_certfile="./cert.pem",
                log_level="info")


if __name__ == "__main__":
    #import_1c()

    scheduler = AsyncIOScheduler()
    #scheduler.add_job(thr)
    #scheduler.add_job(thread.getCncStatus, 'interval', seconds=3)
    scheduler.add_job(start_uvicorn)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    '''
    '''