from pydantic import BaseModel
from typing import Optional


class ProcessRequest(BaseModel):
    file_id: Optional[str] = None
    chunk_size: Optional[int] = 400
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0  # 1 to delete old chunks, 0 to keep old chunks
