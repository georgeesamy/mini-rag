from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId  # specific id type for MongoDB
from datetime import datetime


class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(gt=0, default=0)  # greater than 0
    asset_config: dict = Field(default_factory=dict)  # default is an empty dict
    asset_pushed_at: datetime = Field(default_factory=datetime.utcnow)  # default is the current time

    class Config:
        arbitrary_types_allowed = True  # this allows us to use the ObjectId type in our model

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("asset_project_id", 1)],  # this creates an index on the project_id field in ascending order
                "name": "asset_project_id_index_1",  # this is the name of the index
                "unique": False,  # this ensures that the project_id is unique in the collection
            },
            {
                "key": [
                    ("asset_project_id", 1),
                    ("asset_name", 1),
                ],
                "name": "asset_project_id_name_index_1",  # this is the name of the index
                "unique": True,  # this ensures that the project_id is unique in the collection
            },
        ]
