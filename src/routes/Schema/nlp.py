from typing import Optional

from pydantic import BaseModel


class PushRequest(BaseModel):
    do_reset: bool = False

class SearchRequest(BaseModel):
    text: str
    limit:int = 5