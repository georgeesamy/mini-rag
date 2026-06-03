from pydantic import BaseModel
from typing import Optional


class ProcessRequest(BaseModel):
    file_id: Optional[str] = None
    chunk_size: int = 400
    overlap_size: int = 20
    do_reset: int = 0  # 1 to delete old chunks, 0 to keep old chunks
