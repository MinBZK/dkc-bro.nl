"""First setup expert service db

Revision ID: 6dd85657c2c4
Revises: 
Create Date: 2021-10-06 11:38:59.376191

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "6dd85657c2c4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "rule",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("object_type", sa.String(), nullable=True),
        sa.Column("importance", sa.Integer(), nullable=True),
        sa.Column("feedbackMessage", sa.String(), nullable=True),
        sa.Column("explanation", sa.String(), nullable=True),
        sa.Column("ruleType", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rule_id"), "rule", ["id"], unique=False)
    op.create_table(
        "finding",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("result", sa.Boolean(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("filename", sa.String(), nullable=True),
        sa.Column("rule_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["rule_id"],
            ["rule.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_finding_filename"), "finding", ["filename"], unique=False)
    op.create_index(op.f("ix_finding_id"), "finding", ["id"], unique=False)
    op.create_index(op.f("ix_finding_result"), "finding", ["result"], unique=False)
    op.create_index(
        op.f("ix_finding_timestamp"), "finding", ["timestamp"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_finding_timestamp"), table_name="finding")
    op.drop_index(op.f("ix_finding_result"), table_name="finding")
    op.drop_index(op.f("ix_finding_id"), table_name="finding")
    op.drop_index(op.f("ix_finding_filename"), table_name="finding")
    op.drop_table("finding")
    op.drop_index(op.f("ix_rule_id"), table_name="rule")
    op.drop_table("rule")
    # ### end Alembic commands ###
