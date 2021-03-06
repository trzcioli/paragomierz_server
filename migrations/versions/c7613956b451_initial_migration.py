"""Initial migration.

Revision ID: c7613956b451
Revises: 0badef111c25
Create Date: 2020-07-06 20:20:43.392233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7613956b451'
down_revision = '0badef111c25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('api_key', sa.String(length=500), nullable=True),
    sa.Column('url_api_key', sa.String(length=500), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_index(op.f('ix_user_api_key'), 'user', ['api_key'], unique=True)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_url_api_key'), 'user', ['url_api_key'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_url_api_key'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_api_key'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
