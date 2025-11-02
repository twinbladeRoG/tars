# TARS FastAPI Backend

# Getting Started

## Installation

### Install [UV](https://docs.astral.sh/uv/) - Rust based python package manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Create Virtual Environment for Python using UV

```bash
uv venv
source .venv/bin/activate
```

### Install dependencies

```bash
uv sync
```

## Dependencies

| Package                                              | Description        |
| ---------------------------------------------------- | ------------------ |
| [Alembic](https://alembic.sqlalchemy.org/en/latest/) | Database Migration |

## Managing Migrations using Alembic

To create new migration

```bash
uv run alembic revision --autogenerate -m "add user table"
```

To run your migrations

```bash
uv run alembic upgrade head
```

To check migration history

```bash
uv run alembic history --verbose
```

To downgrade to beginning

```bash
uv run alembic downgrade base
```

## Running local LLM server with llama-cpp

### Start Embedding Server

```sh
./llama-server -m ../../models/bge-large-en-v1.5_fp32.gguf --embedding --pooling cls -ub 8192 --port 9090
```

### Start LLM Server

```sh
./llama-server -m ../../models/Qwen3-14B-Q6_K.gguf --port 8090 --jinja -ngl 35
```

## Development / Debug

| Package                                             | Description                                |
| --------------------------------------------------- | ------------------------------------------ |
| [Qdrant Dashboard](http://localhost:6333/dashboard) | Inspect all vector points stored in Qdrant |
| [Redis Commander](http://localhost:8082/)           | Inspect data store in redis memory         |
| [PgAdmin](http://localhost:5050/)                   | Admin panel for PostgresSQL DB             |
| [Adminer](http://localhost:8080/)                   | Simple admin panel for SQL-based Databases |
| [Kafbat UI](http://localhost:8081/)                 | Admin panel you Kafka instances            |
| [Flower](http://localhost:5555/)                    | Celery Flower                              |

## Celery

Run celery worker:

```sh
uv run celery -A src.celery.tasks worker --loglevel=INFO
```

Run celery flower:

```sh
uv run celery -A src.celery.tasks flower
```

## Installing `scapy`

```bash
uv pip install --no-build-isolation --force-reinstall spacy
uv add scapy
```

```bash
python -m ensurepip --default-pip

# spaCy
python -m spacy download en_core_web_sm

# nltk
python -m nltk.downloader words
python -m nltk.downloader stopwords
```
