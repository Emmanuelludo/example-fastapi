"""create users table

Revision ID: 1dfba2ad8949
Revises:
Create Date: 2021-12-24 17:57:17.246643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dfba2ad8949'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("Users", sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('email', sa.String, nullable=False, unique=True), sa.Column(
        'password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_table('Users')
    pass
