"""extend tables with extra columns

Revision ID: 9d1aa1c4586b
Revises: a9af9fde377c
Create Date: 2023-09-24 17:47:02.265408

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9d1aa1c4586b"
down_revision: Union[str, None] = "a9af9fde377c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("orders", sa.Column("code", sa.String(length=20), nullable=False))
    op.add_column("orders", sa.Column("start_date", sa.DateTime(), nullable=False))
    op.add_column("users", sa.Column("superuser", sa.Boolean(), nullable=False))
    op.add_column("users", sa.Column("active", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "active")
    op.drop_column("users", "superuser")
    op.drop_column("orders", "start_date")
    op.drop_column("orders", "code")
    # ### end Alembic commands ###
