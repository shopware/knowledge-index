from typing import Union
from fastapi import FastAPI, UploadFile, Query, Form, Body
from fastapi.middleware.cors import CORSMiddleware

import zipfile
import aiofiles
import os
import glob
import shutil

from .upload import upload
from .query import query, query_by_id, map_results
from .ingest import ingest, ingest_diff, ingest_url
from .config import data_dir
from .params import (
    SearchParam,
    CollectionParam,
    PostQueryParams,
    PostNeighboursParams,
    PostURLIngestParams,
)
from .results import Results, Result, Success, Hello, Status

import logging

description = """
Shopware document ingestion and querying API allows you to:
 - upload .md documents,
 - organize them in collections,
 - store their vector embeddings from OpenAI API or Tensorflow,
 - and run similarity search afterwards.
"""

tags_metadata = [
    {"name": "root", "description": "Hello World demo endpoint"},
    {"name": "upload", "description": ""},
    {"name": "ingest", "description": ""},
    {"name": "ingest-diff", "description": ""},
    {"name": "query", "description": ""},
    {"name": "neighbours", "description": ""},
    {"name": "healthcheck", "description": ""},
]

app = FastAPI(
    title="Shopware document ingestion and querying API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Shopware",
        "url": "https://shopware.com/contact/",
        "email": "developer@shopware.com",
    },
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="^(http:\/\/localhost(:\d+)?|https?:\/\/[a-zA-Z0-9-]+\.shopware\.com|https?:\/\/[a-zA-Z0-9-]+\.vercel\.app)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
def read_root() -> Hello:
    return {"Hello": "World"}


@app.post("/upload-input", tags=["upload"])
async def post_upload_input(
    content: UploadFile,
    collection: Union[CollectionParam, None, str] = CollectionParam(),
):
    # workaround - https://fastapi.tiangolo.com/tutorial/request-forms-and-files/#define-file-and-form-parameters
    if isinstance(collection, Union[str, None]):
        collection = CollectionParam(collection=collection)

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

    return {"length": length, "collection": collection.collection}


@app.post("/ingest", tags=["ingest"])
def post_ingest(collection: CollectionParam = CollectionParam()) -> Success:
    return {"success": ingest(collection.collection)}


@app.post("/ingest-diff", tags=["ingest-diff"])
def post_ingest(collection: CollectionParam = CollectionParam()) -> Success:
    return {"success": ingest_diff(collection.collection)}


@app.post("/query", tags=["query"])
def post_query(data: PostQueryParams) -> Results:
    results = query(data.search, data.collection)

    return {"results": map_results(results)}


@app.post("/neighbours", tags=["neighbours"])
def post_query(data: PostNeighboursParams) -> Results:
    results = query_by_id(data.id, data.collection)
    results = [result for result in results if result[0].metadata["source"] != data.id]

    return {"results": map_results(results)}


@app.post("/ingest-url")
def ingest_urls(data: PostURLIngestParams):
    return {"success": ingest_url(data.url, data.collection)}


# https://ahmadrosid.com/blog/deploy-fastapi-flyio
# https://fly.io/docs/languages-and-frameworks/python/
# https://fly.io/docs/languages-and-frameworks/dockerfile/
# https://fly.io/docs/reference/secrets/#setting-secrets
@app.get("/healthcheck", tags=["healthcheck"])
def healthcheck() -> Status:
    return {"status": "ok"}
