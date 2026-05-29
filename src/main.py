from fastapi import FastAPI
from .routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from .helpers import get_settings

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)  # open connection to mogodb
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]  # select the project db specifficaly to use
    # both stored in app so any route can use it


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()  # close connection to mongodb


app.include_router(base.base_router)
app.include_router(data.data_router)
