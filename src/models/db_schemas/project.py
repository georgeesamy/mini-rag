from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from bson.objectid import ObjectId  # specific id type for MongoDB


class Project(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @field_validator('project_id')
    @classmethod
    def validate_project_id(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("project_id", 1)],  # this creates an index on the project_id field in ascending order
                "name": "project_id_index_1",  # this is the name of the index
                "unique": True,  # this ensures that the project_id is unique in the collection
            }
        ]
