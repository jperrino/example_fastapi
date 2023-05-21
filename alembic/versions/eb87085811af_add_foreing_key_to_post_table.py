"""add foreing key to post table

Revision ID: eb87085811af
Revises: cbc7eed3e5ef
Create Date: 2023-05-20 17:57:26.120596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb87085811af'
down_revision = 'cbc7eed3e5ef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('postss',
                  sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("postss_userss_fk",
                          source_table='postss',
                          referent_table='userss',
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('postss_userss_fk', table_name='postss')
    op.drop_column('postss', column_name='owner_id')
    pass
