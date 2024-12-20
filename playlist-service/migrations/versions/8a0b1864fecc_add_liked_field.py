"""add liked field

Revision ID: 8a0b1864fecc
Revises: 420aed1d44bc
Create Date: 2024-12-20 22:49:55.630603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a0b1864fecc'
down_revision: Union[str, None] = '420aed1d44bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('playlists', sa.Column('is_liked', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.alter_column('playlists', 'thumbnail',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('playlists', 'thumbnail',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('playlists', 'is_liked')
    # ### end Alembic commands ###
