from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson.objectid import ObjectId


class DataChunk(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    id: Optional[ObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId = Field(...)
    chunk_asset_id: ObjectId

    @classmethod  # static method which do not need class intialization and can be called on the class itself
    def get_indexes(cls):
        return [
            {
                "key": [("chunk_project_id", 1)],  # this creates an index on the chunk_project_id field in ascending order
                "name": "chunk_project_id_index_1",  # this is the name of the index
                "unique": False,  # this ensures that the chunk_project_id is unique in the collection
            }
        ]
    
class RetrievedDocument(BaseModel):
    text: str
    score: float
    