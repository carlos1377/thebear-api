"""nullable OrdemItem FKs

Revision ID: e0888f99f624
Revises: 5934348d558c
Create Date: 2024-05-04 05:07:37.140372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e0888f99f624'
down_revision: Union[str, None] = '5934348d558c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_items', 'order_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('order_items', 'product_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'order_items', 'orders', ['order_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'order_items', 'products', ['product_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order_items', type_='foreignkey')
    op.drop_constraint(None, 'order_items', type_='foreignkey')
    op.alter_column('order_items', 'product_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('order_items', 'order_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
