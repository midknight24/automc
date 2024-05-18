"""add model_vendor column

Revision ID: 6d0146d6d35f
Revises: 4c884b5f785a
Create Date: 2024-05-19 02:40:24.241647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '6d0146d6d35f'
down_revision: Union[str, None] = '4c884b5f785a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('llmbackend', sa.Column('model_vendor', sa.Enum('OPENAI', 'CLAUDE', name='modelvendor'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('llmbackend', 'model_vendor')
    # ### end Alembic commands ###
