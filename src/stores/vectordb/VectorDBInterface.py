from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.db_schemas import RetrievedDocument

class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def does_collection_exist(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self) -> List:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass

    @abstractmethod
    def create_collection(self, collection_name: str,
                          embedding_size: int,
                          do_reset: bool = False):
        pass

    @abstractmethod
    def insert_one(self, collection_name: str,
                       texts:str,
                       vector: List,
                       metadata: Optional[dict]=None,
                       record_ids: Optional[str]=None):
        pass 

    @abstractmethod
    def insert_many(self, collection_name: str, 
                    text:list,
                    vector: list, metadata: Optional[dict]=None,
                    record_id: Optional[str]=None, 
                    batch_size: int = 50):
        pass  

    @abstractmethod
    def search_by_vector(self, collection_name: str,
                         vector: List,
                         limit: int):
        pass

    
