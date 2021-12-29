"""create votes table

Revision ID: dbaa5e159ace
Revises: 487ac674b53f
Create Date: 2021-12-28 17:34:16.505527

"""
from alembic import op
import sqlalchemy as sa

from app.models import Votes


# revision identifiers, used by Alembic.
revision = 'dbaa5e159ace'
down_revision = '487ac674b53f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Votes', sa.Column('owner_id', sa.Integer(
    ), nullable=False, primary_key=True), sa.Column('post_id', sa.Integer(), nullable=False, primary_key=True))
    op.create_foreign_key('Users_owner_id_fkey', source_table='Votes', referent_table='Users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    op.create_foreign_key('PostsOrm_post_id_fkey', source_table='Votes', referent_table='PostsOrm', local_cols=[
                          'post_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('PostsOrm_post_id_fkey', table_name='Votes')
    op.drop_constraint('Users_owner_id_fkey', table_name='Votes')
    op.drop_table('Votes')
    pass
