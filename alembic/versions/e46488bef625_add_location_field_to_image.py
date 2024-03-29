"""add location field to image

Revision ID: e46488bef625
Revises: b4c5127c9684
Create Date: 2024-03-20 15:06:56.169659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e46488bef625'
down_revision: Union[str, None] = 'b4c5127c9684'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('image', sa.Column('location', sa.String, index=True))


def downgrade() -> None:
    pass
