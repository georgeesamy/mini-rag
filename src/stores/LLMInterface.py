#we will use factory architectures 
#we will make an interface which will have not logic
# #interface = contract that the class must follow(shklha) 

from abc import ABC, abstractmethod
from typing import Optional, List

class LLMInterface(ABC):

    @abstractmethod #decorator used to make sure that the method is implemented when a child class implements(not inherets because it has no logic so we say implement) from this interface
    def set_generation_model(self, model_id: str):
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: Optional[List]=None, 
                      max_output_tokens: Optional[int]=None, 
                      temperature: Optional[float]=None):
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: Optional[str] = None): #doc type (query or text chunks (context))
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass

    