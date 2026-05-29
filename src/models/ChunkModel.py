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
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))  # insert_one and some other methods here is from motor which used to make changes in mongodb
        chunk._id = result.inserted_id
        return chunk

    async def get_chunk(self, chunk_id: str):
        record = await self.collection.find_one({
            "_id": ObjectId(chunk_id),
        })  # mongodb uses _id as the default primary key field, and it is of type ObjectId

        if record is None:
            return None

        return DataChunk(**record)  # to convert the record from dictionary to a DataChunk object

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            operations = [InsertOne(chunk.dict(by_alias=True, exclude_unset=True)) for chunk in batch]  # create a list of InsertOne operations for each chunk in the batch
            await self.collection.bulk_write(operations)  # execute the bulk write operation to insert the batch of chunks into the database

            return len(chunks)

    async def delete_chunk_by_project_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({
            "chunk_project_id": project_id,
        })
        return result.deleted_count
