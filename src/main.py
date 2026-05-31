from fastapi import FastAPI
from .routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from .helpers import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)  # open connection to mogodb
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]  # select the project db specifficaly to use
    # both stored in app so any route can use it

    llm_provider_factory = LLMProviderFactory(settings)

    #generation client
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_model(model_id = settings.GENERATION_MODEL_ID)  # set the model to use for generation

    #embedding client
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_model(model_id = settings.EMBEDDING_MODEL_ID,
                                   embedding_size = settings.EMBEDDING_MODEL_EMBEDDING_SIZE)  # set the model to use for embedding

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()  # close connection to mongodb


app.include_router(base.base_router)
app.include_router(data.data_router)
