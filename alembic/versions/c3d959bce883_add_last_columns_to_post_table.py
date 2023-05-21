"""add last columns to post table

Revision ID: c3d959bce883
Revises: eb87085811af
Create Date: 2023-05-20 18:04:57.598619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3d959bce883'
down_revision = 'eb87085811af'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('postss',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('postss',
                  sa.Column('created_at',
                            sa.TIMESTAMP(timezone=True),
                            nullable=False,
                            server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('postss', column_name='published')
    op.drop_column('postss', column_name='created_at')
    pass
