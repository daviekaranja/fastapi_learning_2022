"""create posts table

Revision ID: cd6dc21c032d
Revises: 
Create Date: 2022-06-22 23:35:11.318543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd6dc21c032d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.Integer(), nullable=False))
    pass


def downgrade() -> None:
    pass
