from typing import Union
from fastapi import Body, UploadFile
from pydantic import BaseModel

class IdQuery(BaseModel):
    id: str

class SearchParam(BaseModel):
    search: str = Body(
        min_length=3,
        max_length=128,
        example={
            "search": "my search keywords"
        }
    )


class CollectionParam(BaseModel):
    collection: Union[str, None] = Body(
        default=None,
        min_length=3,
        max_length=128,
        regex="^([a-z0-9]{3,40}|--[a-z0-9]{3,40}|[a-z0-9]{1,40}--[a-z0-9]{1,40}|[a-z0-9]{3,40}--[a-z0-9]{1,40}--[a-z0-9_]{1,40})$",
        example={
            "collection": "test"
        }
    )
    class Config:
        schema_extra = {
            "example": {
                "default": {
                    "collection": None
                },
                "standard": {
                    "collection": "mycollection123"
                },
                "grouped": {
                    "collection": "mycollection123--foo"
                },
                "repository": {
                    "collection": "shopware--docs--main"
                }
            }
        }


class PostQueryParams(CollectionParam, SearchParam):
    class Config:
        schema_extra = {
            "example": {
                "default": {
                    "search": "my search keywords",
                    "collection": None
                },
                "standard": {
                    "search": "my search keywords",
                    "collection": "mycollection123"
                },
                "grouped": {
                    "search": "my search keywords",
                    "collection": "mycollection123--foo"
                },
                "repository": {
                    "search": "my search keywords",
                    "collection": "shopware--docs--main"
                }
            }
        }

class PostNeighboursParams(CollectionParam, IdQuery):
    class Config:
        schema_extra = {
            "example": {
                "default": {
                    "id": "my/document/foo",
                    "collection": None
                },
                "standard": {
                    "id": "my/document/foo",
                    "collection": "mycollection123"
                },
                "grouped": {
                    "id": "my/document/foo",
                    "collection": "mycollection123--foo"
                },
                "repository": {
                    "id": "my/document/foo",
                    "collection": "shopware--docs--main"
                }
            }
        }
