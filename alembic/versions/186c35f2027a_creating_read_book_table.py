"""creating_read_book_table

Revision ID: 186c35f2027a
Revises: cba1b95358d0
Create Date: 2023-03-01 16:19:50.905505+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '186c35f2027a'
down_revision = 'cba1b95358d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "Books_read",
        sa.Column("book_id",
                  postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id",
                  postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("read_date", sa.DateTime, nullable=True),
        sa.PrimaryKeyConstraint('book_id','user_id')
    )


def downgrade() -> None:
    op.drop_table('Books_read')
