from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine
from app.search.elasticsearch_service import es_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'Starting {settings.ENVIRONMENT} environment')
    try:   # Проверка подключения к базе данных
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("Database успешно подключена")
    except Exception as e:
        print(f"Database ошибка при подключении: {e}")
        raise e

    try:   # Проверка подключения к Elasticsearch
        es_service.connect()
        print("Elasticsearch Успешно подключен и индекс создан")
    except Exception as e:
        print(f"Elasticsearch ошибка при подключении: {e}")
        raise e

    yield

    print(f'Ошибка в {settings.ENVIRONMENT} подключении к Elasticsearch')
    await engine.dispose()

app = FastAPI(
    title="Docs Search Test Case",
    description="API для поиска документов",
    version="1.0.0",
    lifespan=lifespan
)


@app.get('/health', summary="Проверка состояния приложения")
async def health_check():
    '''Эндпоинт для проверки состояния приложения'''
    return {"status": "ok"}
