"""add foreign key to the posts table

Revision ID: 81f66b341a5f
Revises: 85a686c933aa
Create Date: 2022-06-23 00:28:14.092050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81f66b341a5f'
down_revision = '85a686c933aa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # added a owner_id column and set a foreign key
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fkey', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
