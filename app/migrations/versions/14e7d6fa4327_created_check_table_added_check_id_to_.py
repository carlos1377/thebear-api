"""created Check table, added check_id to Order table and updated Order_Item table to do not use client_id

Revision ID: 14e7d6fa4327
Revises: c40df5fd3add
Create Date: 2024-05-01 23:52:31.991506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '14e7d6fa4327'
down_revision: Union[str, None] = 'c40df5fd3add'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('checks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('in_use', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('order_items_ibfk_3', 'order_items', type_='foreignkey')
    op.drop_column('order_items', 'client_id')
    op.drop_column('order_items', 'id')
    op.add_column('orders', sa.Column('check', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'orders', 'checks', ['check'], ['id'], ondelete='SET NULL')
    op.drop_column('orders', 'mesa')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('mesa', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'check')
    op.add_column('order_items', sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False))
    op.add_column('order_items', sa.Column('client_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('order_items_ibfk_3', 'order_items', 'clients', ['client_id'], ['id'], ondelete='SET NULL')
    op.drop_table('checks')
    # ### end Alembic commands ###
