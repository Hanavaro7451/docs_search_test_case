from typing import List

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rubrics: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    create_date: Mapped[str] = mapped_column(String, nullable=False)
