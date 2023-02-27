from typing import Union
from fastapi import Body, UploadFile
from pydantic import BaseModel


class SearchParam(BaseModel):
    search: str = Body(min_length=3, max_length=128)


class CollectionParam(BaseModel):
    collection: Union[str, None] = Body(default=None, min_length=3, max_length=128,
                                        regex="^([a-z0-9]{3,40}|--[a-z0-9]{3,40}|[a-z0-9]{1,40}--[a-z0-9]{1,40}|[a-z0-9]{3,40}--[a-z0-9]{1,40}--[a-z0-9_]{1,40})$")


class PostQueryParams(CollectionParam, SearchParam):
    pass
