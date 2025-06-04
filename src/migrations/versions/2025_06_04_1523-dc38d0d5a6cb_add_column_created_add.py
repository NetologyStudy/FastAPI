"""Add column created_add

Revision ID: dc38d0d5a6cb
Revises: cb25fb666906
Create Date: 2025-06-04 15:23:06.244517

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dc38d0d5a6cb"
down_revision: Union[str, None] = "cb25fb666906"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column(
            "created_add",
            sa.DateTime(),
            server_default=sa.text("LOCALTIMESTAMP"),
            nullable=False,
        ),
    )


def downgrade() -> None:

    op.drop_column("bookings", "created_add")

