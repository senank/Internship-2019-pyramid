"""Added user table

Revision ID: 018785bd6dba
Revises: 61d07a943254
Create Date: 2019-08-12 10:28:57.139984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '018785bd6dba'
down_revision = '61d07a943254'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False, unique=True),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('permissions', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('user_id', name=op.f('pk_user'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
