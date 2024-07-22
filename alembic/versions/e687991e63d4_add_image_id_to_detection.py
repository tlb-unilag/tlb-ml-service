"""add image_id to detection

Revision ID: e687991e63d4
Revises: da5ade088715
Create Date: 2024-05-24 09:59:55.142794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e687991e63d4'
down_revision: Union[str, None] = 'da5ade088715'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('detection', sa.Column('image_id', sa.String, index=True))
    op.create_foreign_key(
        None,
        'detection', 'image',
        ['image_id'], ['image_id'],
    )


def downgrade() -> None:
    pass
