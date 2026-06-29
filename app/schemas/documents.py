

from pydantic import BaseModel


class DocumentBase(BaseModel):
    '''Базовая модель документа'''
    id: int
    rubrics: list[str]
    text: str
    create_date: str
