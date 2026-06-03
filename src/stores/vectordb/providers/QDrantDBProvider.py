from qdrant_client import QdrantClient, models
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging
from typing import List, Optional
from uuid import uuid4
from src.models.db_schemas import RetrievedDocument


class QDrantDB(VectorDBInterface):

    def __init__(self, db_path:str, distance_method:str):

        self.client = None
        self.db_path = db_path
        self.distance_method: models.Distance

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT
        else:
            raise ValueError(f"Unsupported distance method: {distance_method}")

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)   

    def disconnect(self):
        self.client = None

    def does_collection_exist(self, collection_name: str) -> bool:
        if self.client is None:
            return False
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> List:
        if self.client is None:
            return []
        return self.client.get_collections().collections
    
    def get_collection_info(self, collection_name: str) -> dict:
        if self.client is None:
            return {}
        return self.client.get_collection(collection_name=collection_name).dict()
    
    def delete_collection(self, collection_name: str):
        if self.client is None:
            return None
        if self.does_collection_exist(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        
    def create_collection(self, collection_name: str,
                          embedding_size: int,
                          do_reset: bool = False):
        
        if self.client is None:
            self.logger.error("Qdrant client is not connected")
            return None

        if do_reset:
            _ = self.delete_collection(collection_name = collection_name) 

        if not self.does_collection_exist(collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method
                )
            )
            return True
        
        return False
    
    def insert_one(self, 
                    collection_name: str,
                    text:str,
                    vector: List,
                    metadata: Optional[dict]=None,
                    record_id: Optional[List[str]]=None):  

        if self.client is None:
            self.logger.error("Qdrant client is not connected")
            return False

        if not self.does_collection_exist(collection_name):
            self.logger.error(f"Collection {collection_name} does not exist")
            return False
        
        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.PointStruct(
                        id=record_id[0] if record_id else str(uuid4()),
                        vector=vector,
                        payload={
                            "text": text, "metadata": metadata}
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error inserting record: {e}")
            return False
        return True
    
    def insert_many(self, collection_name: str,
                       texts: List[str],
                       vectors: List[List],
                       metadata: Optional[List[dict]]=None,
                       record_ids: Optional[List[Optional[str]]]=None,
                       batch_size: int = 50):

        if self.client is None:
            self.logger.error("Qdrant client is not connected")
            return False

        if not self.does_collection_exist(collection_name):
            self.logger.error(f"Collection {collection_name} does not exist")
            return False

        if metadata is None:
            metadata = [{} for _ in texts]

        if record_ids is None:
            record_ids = [str(uuid4()) for _ in texts]

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = [rid if rid is not None else str(uuid4()) for rid in record_ids[i:batch_end]]

            batch_records = [
                models.PointStruct(
                    id=rid,
                    vector=vec,
                    payload={"text": text, "metadata": meta}
                )
                for text, vec, meta, rid in zip(batch_texts, batch_vectors, batch_metadata, batch_record_ids)
            ]
            
            try:
                _ = self.client.upsert(
                    collection_name=collection_name,
                    points=batch_records,
                )
            except Exception as e:
                self.logger.error(f"Error inserting batch: {e}")
                return False    
        return True
    
    def search_by_vector(self, collection_name: str, vector: List, limit: int = 5):
        if self.client is None:
            self.logger.error("Qdrant client is not connected")
            return []
        
        results = self.client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit
        )
    
        if results is None or not getattr(results, "points", None):
            return None

        return [
            RetrievedDocument(
                text=point.payload.get("text", ""),
                score=point.score
            )
            for point in results.points
        ]