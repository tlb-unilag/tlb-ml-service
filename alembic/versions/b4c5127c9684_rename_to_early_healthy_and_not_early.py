"""rename to early, healthy and not_early

Revision ID: b4c5127c9684
Revises: 
Create Date: 2024-03-07 15:32:55.189654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4c5127c9684'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('detection', sa.Column('early', sa.Integer))
    op.add_column('detection', sa.Column('healthy', sa.Integer))
    op.add_column('detection', sa.Column('not_early', sa.Integer))


def downgrade() -> None:
    op.drop_column('detection', 'taro_early')
    op.drop_column('detection', 'taro_late')
    op.drop_column('detection', 'taro_healthy')
    op.drop_column('detection', 'taro_mid')