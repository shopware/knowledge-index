from typing import Union, List, Optional, Dict
from fastapi import Body, UploadFile
from pydantic import BaseModel


class IdQuery(BaseModel):
    id: str

    def get_id(self):
        id = self.id
        if id.endswith('/'):
            return id + "index.md"

        return id


class SearchParam(BaseModel):
    search: str = Body(
        min_length=3, max_length=128, example={"search": "my search keywords"}
    )


class URLParam(BaseModel):
    url: str


class CollectionParam(BaseModel):
    collection: Optional[str] = Body(
        default=None,
#        min_length=3,
        max_length=128,
#        regex="^(|[a-z0-9_]{3,40}|[a-z0-9_]{1,40}--[a-z0-9_]{1,40}|[a-z0-9_]{3,40}--[a-z0-9_]{1,40}--[a-z0-9_]{1,40})$",
        regex="^(|[a-z0-9_\-]{3,128})$",
        example={"collection": "test"},
    )
    collections: List[str] = Body(
        default=[], example={"collections": ["test1", "test2"]}
    )

    class Config:
        schema_extra = {
            "example": {
                "default": {"collection": None},
                "standard": {"collection": "mycollection123"},
                "grouped": {"collection": "mycollection123--foo"},
                "repository": {"collection": "shopware--docs--main"},
            }
        }


class Filter(Dict):
    exclude: List[str]
    include: Optional[List[str]]


class FiltersParam(BaseModel):
    filters: Optional[Dict] = Body(default={})


class PostQueryParams(CollectionParam, SearchParam):
    class Config:
        schema_extra = {
            "example": {
                "default": {"search": "my search keywords", "collection": None},
                "standard": {
                    "search": "my search keywords",
                    "collection": "mycollection123",
                },
                "grouped": {
                    "search": "my search keywords",
                    "collection": "mycollection123--foo",
                },
                "repository": {
                    "search": "my search keywords",
                    "collection": "shopware--docs--main",
                },
                "multi-collection": {
                    "search": "my search keywords",
                    "collections": ["test1", "test2"],
                },
            }
        }


class PostNeighboursParams(CollectionParam, FiltersParam, IdQuery):
    class Config:
        schema_extra = {
            "example": {
                "default": {"id": "my/document/foo", "collection": None},
                "standard": {"id": "my/document/foo", "collection": "mycollection123"},
                "grouped": {
                    "id": "my/document/foo",
                    "collection": "mycollection123--foo",
                },
                "repository": {
                    "id": "my/document/foo",
                    "collection": "shopware--docs--main",
                },
            }
        }


class QuestionParams(CollectionParam):
    q: str


class PostURLIngestParams(CollectionParam, URLParam):
    pass
