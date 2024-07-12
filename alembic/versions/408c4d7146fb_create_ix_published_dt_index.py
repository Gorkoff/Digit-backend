"""Create ix_published_dt index

Revision ID: 408c4d7146fb
Revises: 3a54cde9c1ab
Create Date: 2024-06-23 23:56:32.120157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '408c4d7146fb'
down_revision: Union[str, None] = '3a54cde9c1ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create index ix_published_dt on published_dt column
    op.create_index('ix_published_dt', 'article', ['published_dt'])


def downgrade() -> None:
    # Drop index ix_published_dt
    op.drop_index('ix_published_dt', table_name='article')
