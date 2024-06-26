"""Add batch table

Revision ID: 81a16d547e1e
Revises: bfedade6c570
Create Date: 2021-10-13 17:00:13.396667

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "81a16d547e1e"
down_revision = "bfedade6c570"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "batch",
        sa.Column("id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_batch_id"), "batch", ["id"], unique=False)
    op.add_column("finding", sa.Column("batch_id", sa.String(), nullable=True))
    op.create_foreign_key(None, "finding", "batch", ["batch_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "finding", type_="foreignkey")
    op.drop_column("finding", "batch_id")
    op.drop_index(op.f("ix_batch_id"), table_name="batch")
    op.drop_table("batch")
    # ### end Alembic commands ###
