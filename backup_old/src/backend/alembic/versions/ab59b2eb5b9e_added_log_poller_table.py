"""added log_poller table

Revision ID: ab59b2eb5b9e
Revises: 30e76d1fef2a
Create Date: 2023-06-30 13:59:32.838231

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "ab59b2eb5b9e"
down_revision = "30e76d1fef2a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "log_poller",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("request_url", sa.String(length=255), nullable=True),
        sa.Column("request_status_code", sa.Integer(), nullable=True),
        sa.Column("log_message", sa.String(length=255), nullable=True),
        sa.Column("timestamp", sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("log_poller")
