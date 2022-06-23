"""create users table

Revision ID: 85a686c933aa
Revises: cd6dc21c032d
Create Date: 2022-06-23 00:01:31.577380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85a686c933aa'
down_revision = 'cd6dc21c032d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(),nullable=False ),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
