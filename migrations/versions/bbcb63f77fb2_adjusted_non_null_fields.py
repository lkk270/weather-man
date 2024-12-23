"""adjusted non null fields

Revision ID: bbcb63f77fb2
Revises: 7459b3935fe7
Create Date: 2024-12-08 12:56:24.598289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbcb63f77fb2'
down_revision: Union[str, None] = '7459b3935fe7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('weather_forecasts', 'relative_humidity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('weather_forecasts', 'is_daytime',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('weather_forecasts', 'probability_of_precipitation',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('weather_forecasts', 'short_forecast',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('weather_observations', 'relative_humidity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('weather_observations', 'short_observation',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('weather_observations', 'short_observation',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('weather_observations', 'relative_humidity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('weather_forecasts', 'short_forecast',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('weather_forecasts', 'probability_of_precipitation',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('weather_forecasts', 'is_daytime',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('weather_forecasts', 'relative_humidity',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
    # ### end Alembic commands ###
