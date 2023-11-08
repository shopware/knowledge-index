from typing import Union, Literal
from fastapi import FastAPI, UploadFile, Query, Form, Body, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

import zipfile
import aiofiles
import os
import glob
import shutil
import typer

from .upload import upload
from .query import query, query_by_id, query_n_with_fallback, map_results, unique_results
from .ingest import ingest, ingest_diff, ingest_url
from .cache import prune_cache
from .storage import get_storage_info
from .download import get_download
from .status import get_status
from .config import data_dir
from .exception import EmptyEmbeddings
from .security import require_api_key
from .params import (
    SearchParam,
    CollectionParam,
    PostQueryParams,
    PostNeighboursParams,
    PostURLIngestParams,
    QuestionParams,
)
from .answering import generate_answer
from .results import Results, Result, Success, SuccessWithMetadatas, Hello, Status

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
    {
        "name": "me",
        "description": "Test authentication by providing `X-Shopware-Api-Key` header",
    },
    {
        "name": "upload",
        "description": "Upload a zip file containing .md files to be ingested. A collection name can be provided to organize the documents in multiple indices.",
    },
    {
        "name": "ingest",
        "description": "Ingest a collection of documents. This will create a new index and create and store vector embeddings for each document.",
    },
    {
        "name": "ingest-diff",
        "description": """Ingest unindexed documents of a collection. This will create and store vector embeddings for each uningested document.
If a document is already indexed, it will be skipped, if no document is indexed a new index will be created.""",
    },
    {"name": "ingest-url", "description": ""},
    {
        "name": "query",
        "description": "Query a collection based on a search query. This will return the 5 closest documents based on the vector embeddings.",
    },
    {
        "name": "neighbours",
        "description": """Obtain the closest neighbours for a given document id. This will return the 5 closest documents based on the vector embeddings.
An id is the relative file name of the .md file - for example: `src/docs/products/extensions/migration-assistant/concept/dataselection-and-dataset.md`""",
    },
    {"name": "cache", "description": "Delete old cache from the filesystem"},
    {"name": "storage", "description": "Get storage usage"},
    {"name": "download", "description": "Download <db> or <docs> dir for <collection>"},
    {"name": "question", "description": "Q&A endpoint"},
    {"name": "healthcheck", "description": "Healthcheck endpoint"},
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


@app.get("/me", tags=["me"])
def read_me(token: str = Depends(require_api_key)) -> Success:
    return {"success": True}


@app.post("/upload-input", tags=["upload"])
async def post_upload_input(
    content: UploadFile,
    collection: Union[CollectionParam, None, str] = CollectionParam(),
    token: str = Depends(require_api_key),
):
    # workaround - https://fastapi.tiangolo.com/tutorial/request-forms-and-files/#define-file-and-form-parameters
    if isinstance(collection, Union[str, None]):
        collection = CollectionParam(collection=collection)

    return await upload(content, collection.collection)


@app.post("/ingest", tags=["ingest"])
def post_ingest(
    collection: CollectionParam = CollectionParam(),
#    token: str = Depends(require_api_key),
) -> SuccessWithMetadatas:
    try:
        db = ingest(collection.collection)
    except EmptyEmbeddings:
        return {
            "success": False,
            "metadatas": [],
        }

    return {
        "success": True,
        "metadatas": db.stats["metadatas"],
    }


@app.post("/ingest-diff", tags=["ingest-diff"])
def post_ingest(
    collection: CollectionParam = CollectionParam(),
    token: str = Depends(require_api_key),
) -> Success:
    return {"success": ingest_diff(collection.collection)}


@app.post("/query", tags=["query"])
def post_query(data: PostQueryParams) -> Results:
    results = []
    if data.collections and len(data.collections) > 0:
        for collection in data.collections:
            results += map_results(query(data.search, collection))
    else:
        results = map_results(query(data.search, data.collection))

    results.sort(key=lambda result: float(result["score"]))

    return {"results": unique_results(results)}


@app.post("/neighbours", tags=["neighbours"])
def post_neighbours(data: PostNeighboursParams) -> Results:
    num = 5
    depth = 5
    results = query_n_with_fallback(data.get_id(), data.collection, num, num, depth, data.filters)

    return {"results": unique_results(map_results(results))[0:num]}


@app.post("/ingest-url", tags=["inject-url"])
def ingest_urls(
    data: PostURLIngestParams,
    token: str = Depends(require_api_key),
) -> Success:
    return {"success": ingest_url(data.url, data.collection)}


@app.delete("/cache", tags=["cache"])
def delete_cache(token: str = Depends(require_api_key)) -> Success:
    return {"success": prune_cache()}


@app.get("/storage", tags=["storage"])
def get_storage(token: str = Depends(require_api_key)):
    return get_storage_info()


@app.get("/download/{type}/{collection}", tags=["download"])
def get_storage(
        type: Literal["db", "docs"],
        collection: str,
        token: str = Depends(require_api_key)
):
    return get_download(type, collection)


@app.post("/question", tags=["question"])
def post_question(
    data: QuestionParams,
):
    return generate_answer(data.q)


# https://ahmadrosid.com/blog/deploy-fastapi-flyio
# https://fly.io/docs/languages-and-frameworks/python/
# https://fly.io/docs/languages-and-frameworks/dockerfile/
# https://fly.io/docs/reference/secrets/#setting-secrets
@app.get("/healthcheck", tags=["healthcheck"])
def healthcheck() -> Status:
    return get_status()

# Mount the static files directory
# app.mount("/static", StaticFiles(directory="tmp-data", follow_symlink=True), name="static")
# /list/docs/
# /static/docs/src/test.md
# /download/docs/src/test.md
static_path = Path("/data")
app.mount("/static", StaticFiles(directory="/data", follow_symlink=True), name="static")

# Enable directory listing
@app.get("/list/{subpath:path}", include_in_schema=False)
async def list_directory(subpath: str = ""):
    try:
        full_path = Path(static_path / subpath)

        # Get a list of all files in the directory
        file_list = [str(file.name) for file in full_path.iterdir() if file.is_file()]
        dir_list = [str(file.name) for file in full_path.iterdir() if file.is_dir()]

        return {"files": file_list, "dirs": dir_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Custom route to force download
@app.get("/download/{filename:path}")
async def download_file(filename: str):
    file_path = static_path / filename

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    # Use FileResponse with additional headers for forcing download
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return FileResponse(file_path, headers=headers)