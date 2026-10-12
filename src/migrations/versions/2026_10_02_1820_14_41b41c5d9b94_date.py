"""date

Revision ID: 41b41c5d9b94
Revises: 3fec566b9a18
Create Date: 2026-10-02 18:20:14.125663

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "41b41c5d9b94"
down_revision: str | Sequence[str] | None = "3fec566b9a18"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("bookings", "data_from", new_column_name="date_from")
    op.alter_column("bookings", "data_to", new_column_name="date_to")


def downgrade() -> None:
    op.alter_column("bookings", "date_from", new_column_name="data_from")
    op.alter_column("bookings", "date_to", new_column_name="data_to")
