from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession,
                                    async_sessionmaker,
                                    create_async_engine
                                    )
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def get_db_url() -> str:
    '''Формирует ассинхронную ссылку для  PostgreSQL'''
    return (
        f'postgresql+asyncpg://{settings.POSTGRES_USER}:'
        f'{settings.POSTGRES_PASSWORD}@'
        f'{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}'
        f'/{settings.POSTGRES_NAME}'
    )


engine = create_async_engine(
    get_db_url(),
    echo=settings.DEBUG,
    future=True
    )

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    '''Функция для получения сессии базы данных'''
    async with AsyncSessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    '''Базовый класс для моделей базы данных'''
    pass
