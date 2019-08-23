"""init

Revision ID: 5012d11e936c
Revises: 
Create Date: 2019-08-22 18:40:09.782562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5012d11e936c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('completed', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('completed_date', sa.DateTime(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_todo_item'))
    )
    op.create_index(op.f('ix_todo_item_completed'), 'todo_item', ['completed'], unique=False)
    op.create_index(op.f('ix_todo_item_position'), 'todo_item', ['position'], unique=False)
    op.create_index('todo_item_idx', 'todo_item', [sa.text('completed ASC'), sa.text('position DESC')], unique=False)
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('permissions', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('user_id', name=op.f('pk_user')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_index('todo_item_idx', table_name='todo_item')
    op.drop_index(op.f('ix_todo_item_position'), table_name='todo_item')
    op.drop_index(op.f('ix_todo_item_completed'), table_name='todo_item')
    op.drop_table('todo_item')
    # ### end Alembic commands ###
