"""updated check_id on Order to be able to set null

Revision ID: 5934348d558c
Revises: d95e797e0e97
Create Date: 2024-05-02 02:18:06.907089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5934348d558c'
down_revision: Union[str, None] = 'd95e797e0e97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
