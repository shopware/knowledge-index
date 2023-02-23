from typing import Union
from fastapi import FastAPI, UploadFile

from pydantic import BaseModel

import zipfile
import aiofiles
import os
import glob
import shutil

from .ingest import ingest
from .query import query

import logging


class Query(BaseModel):
    query: str


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload-input")
async def post_upload_input(content: UploadFile):
    input_zip = "input.zip"
    output_dir = "/data"

    if os.path.exists(input_zip):
        os.remove(input_zip)

    length = 0
    async with aiofiles.open(input_zip, "wb") as output:
        while chunk := await content.read(1024):
            length += len(chunk)
            await output.write(chunk)

    if os.path.exists(output_dir):
        files = glob.glob(output_dir + "/*")
        for f in files:
            file_path = os.path.join(output_dir, f)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path) 
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path,)

    with zipfile.ZipFile(input_zip, "r") as zip_ref:
        zip_ref.extractall(output_dir)

    # async do the diff + ingestion + backup

    return {"length": length}


@app.post("/ingest")
def post_ingest():
    return {"success": ingest()}


@app.post("/query")
def post_query(search: Query):
    results = query(search.query)
    mappedResults = []

    for result in results:
        source = result[0].metadata["source"]
        excerpt = result[0].page_content
        score = result[1]
        mappedResults.append({"source": source, "score": str(score)})

    return {"results": mappedResults}


# https://ahmadrosid.com/blog/deploy-fastapi-flyio
# https://fly.io/docs/languages-and-frameworks/python/
# https://fly.io/docs/languages-and-frameworks/dockerfile/
# https://fly.io/docs/reference/secrets/#setting-secrets
@app.get("/healthcheck")
def healtcheck():
    return {"status": "ok"}
