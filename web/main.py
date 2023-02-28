from typing import Union
from fastapi import FastAPI, UploadFile, Query, Form, Body
from fastapi.middleware.cors import CORSMiddleware

import zipfile
import aiofiles
import os
import glob
import shutil

from .upload import upload
from .ingest import ingest, ingest_diff
from .query import query, query_by_id
from .config import data_dir
from .params import SearchParam, CollectionParam, PostQueryParams, PostNeighboursParams

import logging

description = """
Shopware document ingestion and querying API allows you to:
 - upload .md documents,
 - organize them in collections,
 - store their vector embeddings from OpenAI API or Tensorflow,
 - and run similarity search afterwards.
"""

app = FastAPI(
    title="Shopware document ingestion and querying API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Shopware",
        "url": "https://shopware.com/contact/",
        "email": "developer@shopware.com",
    }
)

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
async def post_upload_input(
    content: UploadFile, collection: Union[CollectionParam, None, str] = CollectionParam()
):
    # workaround - https://fastapi.tiangolo.com/tutorial/request-forms-and-files/#define-file-and-form-parameters
    if isinstance(collection, Union[str, None]):
        collection = CollectionParam(collection=collection)

    return upload(content, collection.collection)


@app.post("/ingest")
def post_ingest(collection: CollectionParam = CollectionParam()):
    return {"success": ingest(collection.collection)}


@app.post("/ingest-diff")
def post_ingest(collection: CollectionParam = CollectionParam()):
    return {"success": ingest_diff(collection.collection)}


@app.post("/query")
def post_query(data: PostQueryParams):
    results = query(data.search, data.collection)
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


@app.post("/neighbours")
def post_query(data: PostNeighboursParams):
    results = query_by_id(data.id, data.collection)
    results = [
        result for result in results if result[0].metadata["source"] != data.id
    ]
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
