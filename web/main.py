from typing import Union
from fastapi import FastAPI

from pydantic import BaseModel


from .ingest import ingest
from .query import query

import logging

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ingest")
def post_ingest():
    return {"success": ingest()}


@app.get("/query/{search}")
def get_query(search: str):
    results = query(search)
    mappedResults = []

    for result in results:
        source = result[0].metadata["source"]
        excerpt = result[0].page_content
        score = result[1]
        mappedResults.append({"source": source, "score": str(score)})

    return {"results": mappedResults}


class Query(BaseModel):
    query: str


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
