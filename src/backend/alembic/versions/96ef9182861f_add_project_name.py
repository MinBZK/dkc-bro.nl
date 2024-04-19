"""add project_name

Revision ID: 96ef9182861f
Revises: 59b00394c41f
Create Date: 2024-03-21 16:20:57.606660

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "96ef9182861f"
down_revision = "59b00394c41f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("project", sa.Column("project_name", sa.String(), nullable=True))
    op.add_column(
        "project",
        sa.Column("active", sa.Boolean(), nullable=False, server_default="True"),
    )
    op.add_column("project", sa.Column("source_holder", sa.String(), nullable=True))
    op.add_column(
        "project",
        sa.Column(
            "timestamp", sa.DateTime(), nullable=True, server_default=sa.func.now()
        ),
    )


def downgrade():
    op.drop_column("project", "project_name")
    op.drop_column("project", "timestamp")
    op.drop_column("project", "active")
    op.drop_column("project", "source_holder")
