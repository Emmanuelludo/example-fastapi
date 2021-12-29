"""create posts table

Revision ID: 487ac674b53f
Revises: 1dfba2ad8949
Create Date: 2021-12-24 18:09:37.354035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '487ac674b53f'
down_revision = '1dfba2ad8949'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('PostsOrm', sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('title', sa.String, nullable=False),
                    sa.Column('content', sa.String, nullable=False),
                    sa.Column('published', sa.Boolean,
                              server_default='TRUE', nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()')),
                    sa.Column('owner_id', sa.Integer, sa.ForeignKey(
                        'Users.id', ondelete='CASCADE',), nullable=False),
                    sa.orm.relationship('owner', 'User'))
    pass


def downgrade():
    op.drop_table('PostsOrm')
    pass
