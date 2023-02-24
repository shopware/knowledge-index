from typing import Union
from fastapi import FastAPI, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import zipfile
import aiofiles
import os
import glob
import shutil

from .ingest import ingest, ingest_diff
from .query import query
from .config import data_dir

import logging


class SearchQuery(BaseModel):
    query: str


# 1, 2 or 3 alpha-num strings, separated by --, each part max 40 char in length, lowercase
# , regex="^([a-z0-9]{3,40}|--[a-z0-9]{3,40}|[a-z0-9]{1,40}--[a-z0-9]{1,40}|[a-z0-9]{3,40}--[a-z0-9]{1,40}--[a-z0-9]{1,40})$"
class Collection(BaseModel):
    collection: Union[str, None] = Query(default=None, min_length=3, max_length=128)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="^(http:\/\/localhost(:\d+)?|https?:\/\/[a-zA-Z0-9-]+\.shopware\.com|https?:\/\/[a-zA-Z0-9-]+\.vercel\.app)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload-input")
async def post_upload_input(content: UploadFile, collection: Collection):
    input_zip = "input.zip"
    output_dir = data_dir(collection.collection)

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
                shutil.rmtree(
                    file_path,
                )

    with zipfile.ZipFile(input_zip, "r") as zip_ref:
        zip_ref.extractall(output_dir)

    # async do the diff + ingestion + backup

    return {"length": length}


@app.post("/ingest")
def post_ingest(collection: Collection):
    return {"success": ingest(collection.collection)}


@app.post("/ingest-diff")
def post_ingest(collection: Collection):
    return {"success": ingest_diff(collection.collection)}


@app.post("/query")
def post_query(search: SearchQuery, collection: Collection):
    results = query(search.query, collection.collection)
    mappedResults = []

    for result in results:
        source = result[0].metadata["source"]
        heading = result[0].metadata["heading"]
        excerpt = result[0].page_content
        score = result[1]
        mappedResults.append(
            {"source": source, "score": str(score), "heading": heading}
        )

    return {"results": mappedResults}


# https://ahmadrosid.com/blog/deploy-fastapi-flyio
# https://fly.io/docs/languages-and-frameworks/python/
# https://fly.io/docs/languages-and-frameworks/dockerfile/
# https://fly.io/docs/reference/secrets/#setting-secrets
@app.get("/healthcheck")
def healtcheck():
    return {"status": "ok"}
