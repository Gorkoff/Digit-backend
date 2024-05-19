"""Add index to published_dt

Revision ID: 9e4a7dad2c88
Revises: 19a4f394a8a8
Create Date: 2024-05-19 23:45:14.691191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e4a7dad2c88'
down_revision: Union[str, None] = '19a4f394a8a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
