"""added books table

Revision ID: cba1b95358d0
Revises: 1b85ba1e4496
Create Date: 2023-02-27 09:12:30.860551+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cba1b95358d0'
down_revision = '1b85ba1e4496'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "Book",
    sa.Column("id", postgresql.UUID(as_uuid=True)),
    sa.Column("author_id", postgresql.UUID(as_uuid=True)),
    sa.Column("title", sa.String(), unique=True),
    sa.Column("description", sa.String()),
    sa.Column("category", sa.String()),
    sa.Column("book_file_id",postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column("book_avatar_id", postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column("uploaded_date", sa.DateTime(), nullable=True),
    sa.Column("updated_date", sa.DateTime(), nullable=True)
    )



def downgrade() -> None:
    op.drop_table("Book")
