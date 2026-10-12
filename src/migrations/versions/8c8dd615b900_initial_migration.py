"""initial_migration

Revision ID: 8c8dd615b900
Revises: 
Create Date: 2026-09-28 14:06:02.681200

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '8c8dd615b900'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_table('hotels')
    
