from typing import Union, List, Literal
from pydantic import BaseModel

class Success(BaseModel):
    success: bool

class Result(BaseModel):
    score: str
    heading: str

class Results(BaseModel):
    results: List[Result]

class Status(BaseModel):
    status: Literal["ok"]
    hash: Union[str, None]

class Hello(BaseModel):
    Hello: Literal["World"]