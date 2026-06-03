from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import logging
from bson import ObjectId
from .Schema.nlp import PushRequest, SearchRequest
from ..models.ProjectModel import ProjectModel
from ..models.ChunkModel import ChunkModel
from ..controllers.NLPController import NLPController
from ..models.enums import ResponseSignals

logger = logging.getLogger('uvicorn.error')


nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"],
)

@nlp_router.post("/index/push/{project_id}")
async def index_peoject (request:Request, project_id: str, push_request: PushRequest): #request to access fast api app 

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
        )
    
    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(project_id=project_id)

    if not project:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"signal": ResponseSignals.PROJECT_NOT_FOUND.value})
    

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser
    )

    has_records=True 
    page_no = 1
    inserted_items_count = 0
    idx=0

    while has_records:
        page_chunks = await chunk_model.get_project_chunks(project_id=project.id, page_no=page_no, page_size=10)
        if len(page_chunks):
            page_no+=1
        
        if not page_chunks or len(page_chunks)==0:
            has_records=False
            break

        chunks_ids = list(range(idx, idx+len(page_chunks)))
        idx+=len(page_chunks)

        is_inserted = nlp_controller.index_into_vector_db(chunks=page_chunks, 
                                                project=project,
                                                do_reset=push_request.do_reset,
                                                chunks_ids=chunks_ids)
        
        if not is_inserted:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content={"signal": ResponseSignals.INSERT_INTO_VECTORDB_FAILED.value})
        
        inserted_items_count+=len(page_chunks)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"signal": ResponseSignals.INSERTED_INTO_VECTORDB_SUCCESS.value,
                                 "inserted_items_count": inserted_items_count})

@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(project_id=project_id)

    if not project:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"signal": ResponseSignals.PROJECT_NOT_FOUND.value})

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser
    )

    collection_info = nlp_controller.get_vector_db_collection_info(project=project)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"signal": ResponseSignals.VECTOORDB_COLLECTION_RETREIVED_SUCCESS.value,
                                 "collection_info": collection_info})


@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchRequest):
        project_model = await ProjectModel.create_instance(
            db_client=request.app.db_client
        )

        project = await project_model.get_project_or_create_one(project_id=project_id)

        if not project:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"signal": ResponseSignals.PROJECT_NOT_FOUND.value})

        nlp_controller = NLPController(
            vectordb_client=request.app.vectordb_client,
            generation_client=request.app.generation_client,
            embedding_client=request.app.embedding_client,
            template_parser=request.app.template_parser
        )

        search_results = nlp_controller.search_vectordb_collection(project=project,
                                                                   text=search_request.text,
                                                                   limit=search_request.limit)
        if not search_results:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"signal": ResponseSignals.VECTORDB_SEARCH_FAILED.value})

        return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"signal": ResponseSignals.VECTORDB_SEARCH_SUCCESS.value,
                                    "results": [ result.dict()  for result in search_results ]
                        })

@nlp_router.post("/index/answer/{project_id}")
async def answer_rag(request: Request, project_id: str, search_request: SearchRequest):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    answer, full_prompt, chat_history = nlp_controller.answer_rag_question(
        project=project,
        query=search_request.text,
        limit=search_request.limit,
    )

    if not answer:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignals.RAG_ANSWER_ERROR.value
            }
        )

    return JSONResponse(
        content={
            "signal": ResponseSignals.RAG_ANSWER_SUCCESS.value,
            "answer": answer,
            "full_prompt": full_prompt,
            "chat_history": chat_history
        }
    )