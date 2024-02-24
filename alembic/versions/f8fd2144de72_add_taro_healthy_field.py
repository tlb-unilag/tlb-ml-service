"""add taro_healthy field

Revision ID: f8fd2144de72
Revises: 
Create Date: 2024-02-17 18:08:04.437193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8fd2144de72'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('detection', sa.Column('taro_healthy', sa.Integer))


def downgrade() -> None:
    pass
