from typing import Optional
from .BaseDataModel import BaseDataModel
from .db_schemas import DataChunk
from .enums import DataBaseEnums
from bson import ObjectId
from pymongo import InsertOne  # save action to be excuted later in bulk insert


class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnums.COLLECTION_CHUNK_NAME.value]  # type: ignore
        # we cant call ini_collection in the init because init_collection is async and init is not async and can not be async so we will make new function to call init and ini_collection

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)  # create an instance of the class (called init function)
        await instance.init_collection()  # call the init_collection method to initialize the collection and indexes in the database
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()  # list_collection_names is from motor to get all collection names in the database
        if DataBaseEnums.COLLECTION_CHUNK_NAME.value not in all_collections:
            self.collection = await self.db_client.create_collection(DataBaseEnums.COLLECTION_CHUNK_NAME.value)
            indexes = DataChunk.get_indexes()  # get indexes from the DataChunk schema
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"],
                )  # create indexes in the collection (from motor)

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.model_dump(by_alias=True, exclude_unset=True))
        chunk._id = result.inserted_id
        return chunk

    async def get_chunk(self, chunk_id: str):
        record = await self.collection.find_one({
            "_id": ObjectId(chunk_id),
        })

        if record is None:
            return None

        return DataChunk.model_validate(record)

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100) -> int:
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            operations = [InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True)) for chunk in batch]
            await self.collection.bulk_write(operations)
        return len(chunks)

    async def delete_chunk_by_project_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({
            "chunk_project_id": project_id,
        })
        return result.deleted_count


    async def get_project_chunks(self, project_id: Optional[ObjectId], page_no: int = 1, page_size: int = 50):
        result = await self.collection.find({
            "chunk_project_id": project_id,
        }).skip(
            (page_no - 1) * page_size).limit(page_size).to_list(length=None)
        
        return [DataChunk.model_validate(record) for record in result]