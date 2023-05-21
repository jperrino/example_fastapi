"""create post table

Revision ID: 4562d46fc659
Revises: 
Create Date: 2023-05-17 04:08:17.540965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4562d46fc659'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('postss',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('postss')
    pass
