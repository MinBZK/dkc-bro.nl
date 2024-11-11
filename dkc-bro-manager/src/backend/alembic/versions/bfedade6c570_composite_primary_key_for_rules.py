"""Composite primary key for rules

Revision ID: bfedade6c570
Revises: b15bfbaea59b
Create Date: 2021-10-11 14:27:20.476049

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "bfedade6c570"
down_revision = "b15bfbaea59b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE rule DROP CONSTRAINT rule_pkey CASCADE")
    op.create_primary_key("rule_pkey", "rule", ["id", "object_type"])
    op.add_column("finding", sa.Column("rule_object_type", sa.String(), nullable=True))
    op.create_foreign_key(
        "fk_finding_rule",
        "finding",
        "rule",
        ["rule_id", "rule_object_type"],
        ["id", "object_type"],
    )
    op.alter_column("rule", "object_type", existing_type=sa.VARCHAR(), nullable=False)
    op.create_index(op.f("ix_rule_object_type"), "rule", ["object_type"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE rule DROP CONSTRAINT rule_pkey CASCADE")
    op.create_primary_key("rule_pkey", "rule", ["id"])
    op.drop_index(op.f("ix_rule_object_type"), table_name="rule")
    op.alter_column("rule", "object_type", existing_type=sa.VARCHAR(), nullable=True)
    op.create_foreign_key(
        "finding_rule_id_fkey", "finding", "rule", ["rule_id"], ["id"]
    )
    op.drop_column("finding", "rule_object_type")
    # ### end Alembic commands ###