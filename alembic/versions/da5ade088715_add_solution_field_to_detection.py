"""add solution field to detection

Revision ID: da5ade088715
Revises: e46488bef625
Create Date: 2024-05-23 17:54:09.252670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da5ade088715'
down_revision: Union[str, None] = 'e46488bef625'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('detection', sa.Column('solution', sa.String))


def downgrade() -> None:
    pass
