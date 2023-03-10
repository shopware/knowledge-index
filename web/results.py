from typing import Union, List, Literal, Dict
from pydantic import BaseModel

class Success(BaseModel):
    success: bool

class SuccessWithMetadatas(Success):
    metadatas: Union[List, Dict, None]

class Result(BaseModel):
    id: str
    score: str
    heading: str
    description: Union[str, None]

class Results(BaseModel):
    results: List[Result]

class Status(BaseModel):
    status: Literal["ok"]
    hash: Union[str, None]

class Hello(BaseModel):
    Hello: Literal["World"]