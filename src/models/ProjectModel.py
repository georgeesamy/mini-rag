from .BaseDataModel import BaseDataModel
from .db_schemas import Project
from .enums import DataBaseEnums


class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnums.COLLECTION_PROJECT_NAME.value]  # type: ignore

    # we cant call ini_collection in the init because init_collection is async and init is not async and can not be async so we will make new function to call init and ini_collection

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)  # create an instance of the class (called init function)
        await instance.init_collection()  # call the init_collection method to initialize the collection and indexes in the database
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()  # list_collection_names is from motor to get all collection names in the database
        if DataBaseEnums.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = await self.db_client.create_collection(DataBaseEnums.COLLECTION_PROJECT_NAME.value)
            indexes = Project.get_indexes()  # get indexes from the Project schema
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"],
                )  # create indexes in the collection (from motor)

    async def create_project(self, project: Project) -> Project:
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))  # insert_one and some other methods here is from motor which used to make changes in mongodb
        project.id = result.inserted_id
        return project

    async def get_project_or_create_one(self, project_id: str):
        record = await self.collection.find_one({"project_id": project_id})

        if record is None:
            # Project not found, create a new one
            project = Project(project_id=project_id)  # give project schema input which is id
            project = await self.create_project(project=project)  # call create project method and give it the above line as input
            return project

        project = Project(**record)
        return project

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        # count total number of docs
        total_documents = await self.collection.count_documents({})

        # calc total pages
        total_pages = total_documents // page_size
        if total_documents % page_size != 0:
            total_pages += 1

        # Documents: [1..10] [11..20] [21..30] ...    -> givem that page_size=10
        # skip = (3-1) * 10 = 20  → skips first 20 docs
        # limit = 10              → returns docs 21-30

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)  # cursor to fetch the data from mongodb with pagination (from motor)
        projects = []

        async for documents in cursor:
            projects.append(
                Project(**documents)  # convert each record (dict) to a Project object and add to the list
            )

        return projects, total_pages
