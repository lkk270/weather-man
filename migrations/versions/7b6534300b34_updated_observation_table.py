"""updated observation table

Revision ID: 7b6534300b34
Revises: bd9a31df7cbb
Create Date: 2024-12-05 21:47:18.434523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b6534300b34'
down_revision: Union[str, None] = 'bd9a31df7cbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weather_observations', sa.Column('short_observation', sa.String(), nullable=False))
    op.drop_column('weather_observations', 'is_precipitating')
    op.drop_column('weather_observations', 'is_daytime')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weather_observations', sa.Column('is_daytime', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('weather_observations', sa.Column('is_precipitating', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('weather_observations', 'short_observation')
    # ### end Alembic commands ###
