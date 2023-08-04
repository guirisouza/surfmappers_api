from typing import List

from pydantic import BaseModel


class MessageError(BaseModel):
    error_code: str
    error_message: str


class HttpValidationError(BaseModel):
    class Detail(BaseModel):
        loc: List[str]
        msg: str
        type: str

    error_code: str
    error_message: List[Detail]