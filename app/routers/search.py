from fastapi import APIRouter, Query
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.documents import Document
from app.search.elasticsearch_service import es_service

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get("/")
async def search_dockuments(
    q: str = Query(
        ...,
        min_length=1,
        description="Строка для поиска в документах"
    ),
    limit: int = Query(
        20,
        ge=1,
        le=50,
        description="Количество результатов"
    ),
):
    if not es_service.client:
        return {"error": "Elasticsearch не подключен"}
    search_response = es_service.client.search(
        index=es_service.index_name,
        body={
            "query": {
                "multi_match": {
                    "query": q,
                    "fields": ["text"],
                    "fuzziness": "AUTO"
                }
            },
            "size": limit
        }
    )

    hints = search_response['hits']['hits']
    if not hints:
        return {"message": "Совпадений не найдено"}

    hit_ids = [int(hit['_id']) for hit in hints]

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Document).where(Document.id.in_(hit_ids))
        )
        documents = result.scalars().all()

    documents = sorted(documents, key=lambda x: x.created_date, reverse=True)

    return {
        'results': documents,
        'total': len(documents),
        'query': q
    }


@router.delete("/{document_id}", summary="Удалить документ")
async def delete_document(document_id: int):
    if not es_service.client:
        return {"error": "Elasticsearch не подключен"}

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Document).where(Document.id == document_id)
        )
        doc = result.scalar_one_or_none()
        if not doc:
            return {"error": "Документ не найден"}

        await session.delete(doc)
        await session.commit()

    try:
        es_service.client.delete(
            index=es_service.index_name,
            id=str(document_id)
        )
    except Exception as e:
        return {"error": f"Ошибка при удалении из Elasticsearch: {e}"}

    return {"message": f"Документ с id {document_id} успешно удален"}
