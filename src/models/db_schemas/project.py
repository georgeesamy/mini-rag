from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId  # specific id type for MongoDB


class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)  # required field with minimum length of 1 with any type which is ....

    @validator('project_id')  # this is a validator that checks if the project_id is alphanumeric, if not it raises a ValueError.
    def validate_project_id(cls, value):  # cls= the currunt class and value is the input value
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value

    class Config:
        arbitrary_types_allowed = True  # this allows us to use the ObjectId type in our model
        populate_by_name = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("project_id", 1)],  # this creates an index on the project_id field in ascending order
                "name": "project_id_index_1",  # this is the name of the index
                "unique": True,  # this ensures that the project_id is unique in the collection
            }
        ]
