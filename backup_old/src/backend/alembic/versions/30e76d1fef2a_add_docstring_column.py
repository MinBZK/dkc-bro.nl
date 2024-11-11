"""Add docstring column

Revision ID: 30e76d1fef2a
Revises: 330c2abd5329
Create Date: 2023-02-10 08:56:12.861605

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "30e76d1fef2a"
down_revision = "330c2abd5329"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("rule", sa.Column("docstring", sa.String(), nullable=True))


def downgrade():
    op.drop_column("rule", "docstring")
