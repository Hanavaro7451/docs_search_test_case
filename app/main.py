from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f'Starting {settings.ENVIRONMENT} environment')
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise e
    yield
    print(f'Shutting down {settings.ENVIRONMENT} environment')
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
