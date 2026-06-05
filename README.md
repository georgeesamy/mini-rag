# mini-rag

Minimal RAG (retrieval-augmented generation) API for question answering, built with FastAPI, MongoDB, and Qdrant local storage.

## Requirements

- Python 3.8+ (3.10+ recommended)
- Docker (optional, for local MongoDB)

### Python environment (MiniConda)

1) Install MiniConda: https://docs.anaconda.com/free/miniconda/#quick-command-line-install
2) Create the environment:
```bash
conda create -n mini-rag python=3.10
```
3) Activate it:
```bash
conda activate mini-rag
```

## Install dependencies

From the repo root:
```bash
pip install -r src/requirements.txt
```

## Environment configuration

There are two environment files: one for the API and one for the MongoDB container.

### API env file (required)

Copy the template and edit values:
```bash
copy src\.env.example src\.env
```

macOS/Linux:
```bash
cp src/.env.example src/.env
```

These variables are required by [src/helpers/config.py](src/helpers/config.py). Keep the names in uppercase:

- `APP_NAME`, `APP_VERSION`
- `FILE_ALLOWED_TYPES` (JSON-style list), `FILE_MAX_SIZE`, `FILE_DEFAULT_CHUNK_SIZE`
- `MONGODB_URL`, `MONGODB_DATABASE`
- `GENERATION_BACKEND`, `EMBEDDING_BACKEND`
- `OPENAI_API_KEY`, `OPENAI_API_URL` (optional), `COHERE_API_KEY`
- `GENERATION_MODEL_ID`, `EMBEDDING_MODEL_ID`, `EMBEDDING_MODEL_SIZE`
- `DEFAULT_INPUT_MAX_CHARACTERS`, `DEFAULT_OUTPUT_MAX_CHARACTERS`, `DEFAULT_GENERATION_TEMPERATURE`
- `VECTOR_DB_BACKEND`, `VECTOR_DB_PATH`, `VECTOR_DB_DISTANCE_METHOD`
- `PRIMARY_LANGUAGE`, `DEFAULT_LANGUAGE`

Example values (adjust to your setup):
```env
APP_NAME="mini-RAG"
APP_VERSION="0.1"

FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=512000

MONGODB_URL="mongodb://mini:mini@localhost:27007/?authSource=admin"
MONGODB_DATABASE="mini_rag"

GENERATION_BACKEND="OPENAI"
EMBEDDING_BACKEND="COHERE"

OPENAI_API_KEY=""
OPENAI_API_URL=""
COHERE_API_KEY=""

GENERATION_MODEL_ID="gpt-3.5-turbo-0125"
EMBEDDING_MODEL_ID="embed-multilingual-light-v3.0"
EMBEDDING_MODEL_SIZE=384

DEFAULT_INPUT_MAX_CHARACTERS=1024
DEFAULT_OUTPUT_MAX_CHARACTERS=200
DEFAULT_GENERATION_TEMPERATURE=0.1

VECTOR_DB_BACKEND="QDRANT"
VECTOR_DB_PATH="src/assets/database/qdrant_db"
VECTOR_DB_DISTANCE_METHOD="cosine"

PRIMARY_LANGUAGE="en"
DEFAULT_LANGUAGE="en"
```

### MongoDB env file (if using Docker)

Create a local env file for MongoDB credentials:
```bash
copy docker\.env.example docker\.env
```

macOS/Linux:
```bash
cp docker/.env.example docker/.env
```

Set:
- `MONGO_INITDB_ROOT_USERNAME`
- `MONGO_INITDB_ROOT_PASSWORD`

## Start MongoDB (Docker)

From the repo root:
```bash
docker compose -f docker\docker-compose.yml --env-file docker\.env up -d
```

MongoDB will be available on `localhost:27007` (see [docker/docker-compose.yml](docker/docker-compose.yml)).
Use the same username/password in `MONGODB_URL` (example shown above).

## Run the API

From the repo root:
```bash
uvicorn src.main:app --reload
```

Endpoints:

- Base info: `GET /api/v1/`
- OpenAPI docs: `GET /docs`

## Notes

- The vector database uses local Qdrant storage at `VECTOR_DB_PATH`. Make sure the path exists and is writable.
- If you do not want Docker, set `MONGODB_URL` to your own MongoDB instance.
