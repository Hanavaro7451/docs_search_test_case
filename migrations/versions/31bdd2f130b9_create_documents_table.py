"""create documents table

Revision ID: 31bdd2f130b9
Revises: fc5b768d2aac
Create Date: 2026-06-30 21:15:16.423527
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '31bdd2f130b9'
down_revision: Union[str, Sequence[str], None] = 'fc5b768d2aac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('rubrics', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('created_date', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)
    op.create_index(op.f('ix_documents_created_date'), 'documents', ['created_date'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_documents_created_date'), table_name='documents')
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    op.drop_table('documents')