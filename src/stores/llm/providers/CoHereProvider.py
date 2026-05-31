from stores.llm.LLMInterface import LLMInterface
from stores.llm.LLMEnums import CoHereEnums, DocumentTypeEnums
from typing import Optional, List
import logging
import cohere

class CoHereProvider(LLMInterface):
    def __init__(self, api_key: str, 
                 default_input_max_characters: int = 1000,
                 default_output_max_characters: int = 1000,
                 default_generation_temperature: float = 0.1): 
        
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_characters = default_output_max_characters
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.set_embedding_model_id = None
        self.embbedding_size = None

        self.client = cohere.Client(api_key=self.api_key)
        
        self.logger = logging.getLogger(__name__) # Initialize logger with file name 


    def set_generation_model(self, model_id: str): #we didnt put model_id in init because we can change provider after we run 
        self.generation_model_id = model_id


    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.set_embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()


    def generate_text(self, prompt: str, chat_history: Optional[List] = None, 
                      max_output_tokens: Optional[int] = None, 
                      temperature: Optional[float] = None):
        if not self.client:
            self.logger.error("CoHere client was not set")
            return None
       
        if not self.generation_model_id:
            self.logger.error("Generation model for CoHere was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens is not None else self.default_output_max_characters
        temperature = temperature if temperature is not None else self.default_generation_temperature
        
        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message= self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens)
        
        if not response or not response.text:
            self.logger.error("Error while generating text with CoHere")
            return None 
        return response.text

    def embed_text(self, text: str, document_type: str):
        if not self.client:
            self.logger.error("CoHere client was not set")
            return None
        
        if not self.set_embedding_model_id:
            self.logger.error("Embedding model for CoHere was not set")
            return None
        
        #By defualt text which will get embedd will by of type doc if not specified other wise it will be of type query
        input_type = CoHereEnums.DOCUMENT
        if document_type == DocumentTypeEnums.QUERY:
            input_type =CoHereEnums.QUERY

        response = self.client.embed(
            model=self.set_embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=['float']
        )
        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with CoHere")
            return None
        
        return response.embeddings.float[0]
    

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role, 
            "text": self.process_text(prompt)
        }