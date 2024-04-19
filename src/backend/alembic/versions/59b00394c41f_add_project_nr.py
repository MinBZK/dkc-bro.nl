"""add project_nr

Revision ID: 59b00394c41f
Revises: ab59b2eb5b9e
Create Date: 2024-02-23 18:46:25.346499

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "59b00394c41f"
down_revision = "ab59b2eb5b9e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "project_nr",
            sa.Integer(),
            nullable=False,
            comment="project nummer",
        ),
        sa.Column(
            "environment",
            sa.Enum("DEV", "TEST", "ACC", "PROD", name="environments"),
            nullable=False,
            comment="Omgeving waarin de projecten zich bevinden.",
        ),
    )

    op.add_column("finding", sa.Column("project_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "finding_project_id_fkey",
        "finding",
        "project",
        ["project_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint("finding_project_id_fkey", "finding", type_="foreignkey")
    op.drop_table("project")
    op.drop_column("finding", "project_id")
    op.execute("DROP TYPE IF EXISTS environments")
