from enum import Enum


class ResponseSignals(Enum):
    FILE_VALIDATED_SUCCESS = "file_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_FAILED = "processing_failed"
    PROCESSING_SUCCESS = "processing_success"
    NO_FILES_ERROR = "no_files_found"
    FILE_ID_ERROR = "no_file_found_for_given_id"
    PROJECT_NOT_FOUND = "project_not_found"
    INSERT_INTO_VECTORDB_FAILED = "insert_into_vector_db_failed"
    INSERTED_INTO_VECTORDB_SUCCESS = "inserted_into_vector_db_successfully"
    VECTOORDB_COLLECTION_RETREIVED_SUCCESS = "vector_db_collection_retrieved_successfully"
    VECTORDB_SEARCH_SUCCESS = "vector_db_search_successfully"
    VECTORDB_SEARCH_FAILED = "vector_db_search_failed"
    RAG_RESPONSE_SUCCESS = "rag_response_successfully"
    RAG_RESPONSE_FAILED = "rag_response_failed"
    RAG_ANSWER_ERROR = "rag_answer_error"
    RAG_ANSWER_SUCCESS = "rag_answer_success"