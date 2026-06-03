from fastapi import FastAPI
from .routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from .helpers import get_settings
from .stores.llm.LLMProviderFactory import LLMProviderFactory
from .stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from .stores.llm.templates.template_parser import TemplateParser

app = FastAPI()


@app.on_event("startup")
async def startup_span():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)  # open connection to mogodb
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]  # select the project db specifficaly to use
    # both stored in app so any route can use it

    settings_dict = settings.model_dump()
    llm_provider_factory = LLMProviderFactory(settings_dict)
    vectordb_provider_factory = VectorDBProviderFactory(settings_dict)

    #generation client
    app.generation_client = llm_provider_factory.create_provider(provider_name=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    #embedding client
    app.embedding_client = llm_provider_factory.create_provider(provider_name=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)

    # vector db client
    app.vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vectordb_client.connect()

    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANGUAGE,
        default_language=settings.DEFAULT_LANGUAGE,
    )
    
@app.on_event("shutdown")
async def shutdown_span():
    app.mongo_conn.close()  # close connection to mongodb
    app.vectordb_client.disconnect()  # disconnect from vector database if connected

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)
    