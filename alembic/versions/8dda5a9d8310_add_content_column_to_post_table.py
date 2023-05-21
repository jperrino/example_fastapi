"""add content column to post table

Revision ID: 8dda5a9d8310
Revises: 4562d46fc659
Create Date: 2023-05-17 04:23:41.105834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8dda5a9d8310'
down_revision = '4562d46fc659'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('postss',
                  sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('postss', 'content')
    pass
