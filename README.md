# Document Search Service (DCC)

Поисковая система по тексту документов

## Стек технологий

- **FastAPI**
- **PostgreSQL** + SQLAlchemy 2.0 + asyncpg
- **Elasticsearch** 8.15
- **Docker** + Docker Compose
- **Alembic** (миграции)

## Основные Эндпойнты

- **GET /healh** - проверка состояния
- **GET /search/?q=запрос&limit=20** - поиск по тексту
- **DELETE /search/{id}** - удаление записи

## Инструкция по запуску

### Заполните файл окружения .env

```
    POSTGRES_NAME=docs_search_test_case
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=admin
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
```
*Указан один из примеров заполнения*

### Запуск аркестратора

```bash
    docker-compose up --build -d
```

### Заполнение тестовыми данными Postgres & Elastic

```bash
    docker-compose exec app sh -c "PYTHONPATH=. python scripts/load_data.py"
    docker-compose exec app sh -c "PYTHONPATH=. python scripts/reindex_to_es.py"
```

## Документация 

**Swagger UI** http://localhost:8000/docs
**OpenAPI** docs.json

*Приятного пользования*
*Developed by Hanavaro7451*
