"""Change type column published_dt

Revision ID: 95ae2f780304
Revises: 9e4a7dad2c88
Create Date: 2024-05-19 23:51:24.642496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95ae2f780304'
down_revision: Union[str, None] = '9e4a7dad2c88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Изменение типа колонки с явным преобразованием типа
    op.execute("""
        ALTER TABLE article 
        ALTER COLUMN published_dt 
        TYPE DATE USING published_dt::DATE
    """)
    # Добавление индекса
    op.create_index('idx_published_dt', 'article', ['published_dt'], unique=False)

def downgrade():
    # Удаление индекса
    op.drop_index('idx_published_dt', table_name='article')
    # Возвращение к предыдущему типу данных с VARCHAR
    op.alter_column('article', 'published_dt',
                    existing_type=sa.DATE(),
                    type_=sa.VARCHAR(),
                    existing_nullable=True)