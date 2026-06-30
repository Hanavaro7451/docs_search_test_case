import requests
import asyncio
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.documents import Document


async def simple_reindex():
    '''Скрипт для переиндексации документов в Elasticsearch'''
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Document))
        documents = result.scalars().all()
    for doc in documents:
        requests.put(
            f"http://localhost:9200/documents/_doc/{doc.id}",
            json={
                "text": doc.text,
                "created_date": doc.created_date.isoformat()
            },
            headers={"Content-Type": "application/json"}
        )
        if doc.id % 100 == 0:
            print(f"Проиндексировано {doc.id}")

    print("Готово")

asyncio.run(simple_reindex())
