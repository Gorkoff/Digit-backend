"""initial migration

Revision ID: initial
Revises:
Create Date: 2024-05-21 15:44:03.332171

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('article',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(length=256), nullable=True),
        sa.Column('url', sa.VARCHAR(length=128), nullable=True),
        sa.Column('published_dt', sa.DateTime(), nullable=True),
        sa.Column('currency_curs', sa.FLOAT(), nullable=True),
        sa.Column('text', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('article')
