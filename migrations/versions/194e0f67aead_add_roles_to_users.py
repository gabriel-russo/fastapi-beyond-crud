"""add roles to users

Revision ID: 194e0f67aead
Revises: 61bb384e976f
Create Date: 2024-11-12 15:00:16.781124

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '194e0f67aead'
down_revision: Union[str, None] = '61bb384e976f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.VARCHAR(), server_default='user', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
