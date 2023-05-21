"""add user table

Revision ID: cbc7eed3e5ef
Revises: 8dda5a9d8310
Create Date: 2023-05-20 17:42:40.267897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbc7eed3e5ef'
down_revision = '8dda5a9d8310'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('userss',
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('userss')
    pass
