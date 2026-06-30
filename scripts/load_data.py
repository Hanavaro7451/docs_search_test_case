import csv
import asyncio
from datetime import datetime

from app.db.session import AsyncSessionLocal
from app.models.documents import Document


async def load_csv_data(csv_path: str):
    '''Скрипт для загрузки данных из CSV в базу данных'''
    async with AsyncSessionLocal() as session:
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                try:
                    create_date = datetime.strptime(
                        row['created_date'],
                        '%Y-%m-%d %H:%M:%S'
                    )
                    rubrics_str = row['rubrics'].strip("[]")
                    rubrics = [
                        item.strip(" '")
                        for item in rubrics_str.split(",")
                        if item.strip()
                    ] if rubrics_str else []
                    document = Document(
                        rubrics=rubrics,
                        text=row['text'],
                        created_date=create_date
                    )
                    session.add(document)
                    await session.commit()
                    count += 1

                    if count % 100 == 0:
                        print(f'Загружено {count} документов')

                except Exception as e:
                    await session.rollback()
                    print(f'Ошибка при загрузке документа: {e}')
            print(f'Загрузка данных завершена.'
                  f'Всего загружено документов: {count}')


if __name__ == "__main__":
    csv_file_path = 'data/posts.csv'
    asyncio.run(load_csv_data(csv_file_path))
