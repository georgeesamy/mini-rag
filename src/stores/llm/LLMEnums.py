from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"

class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class CoHereEnums(Enum): #vlaues are in uppercase to match the expected input for cohere's API according to the documentation
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"
    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocumentTypeEnums(Enum):
    DOCUMENT = "document"
    QUERY = "query" 
    