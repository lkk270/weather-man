"""added fields'


Revision ID: 1d0070935037
Revises: 9978f20be798
Create Date: 2024-12-05 18:02:42.103528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d0070935037'
down_revision: Union[str, None] = '9978f20be798'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weather_forecasts', sa.Column('relative_humidity', sa.Float(), nullable=False))
    op.add_column('weather_forecasts', sa.Column('dew_point', sa.Float(), nullable=True))
    op.add_column('weather_forecasts', sa.Column('is_daytime', sa.Boolean(), nullable=False))
    op.add_column('weather_forecasts', sa.Column('probability_of_precipitation', sa.Float(), nullable=False))
    op.add_column('weather_forecasts', sa.Column('short_forecast', sa.String(), nullable=False))
    op.drop_column('weather_forecasts', 'humidity')
    op.add_column('weather_observations', sa.Column('relative_humidity', sa.Float(), nullable=False))
    op.add_column('weather_observations', sa.Column('dew_point', sa.Float(), nullable=True))
    op.add_column('weather_observations', sa.Column('is_daytime', sa.Boolean(), nullable=False))
    op.add_column('weather_observations', sa.Column('is_precipitating', sa.Boolean(), nullable=False))
    op.drop_column('weather_observations', 'humidity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weather_observations', sa.Column('humidity', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('weather_observations', 'is_precipitating')
    op.drop_column('weather_observations', 'is_daytime')
    op.drop_column('weather_observations', 'dew_point')
    op.drop_column('weather_observations', 'relative_humidity')
    op.add_column('weather_forecasts', sa.Column('humidity', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('weather_forecasts', 'short_forecast')
    op.drop_column('weather_forecasts', 'probability_of_precipitation')
    op.drop_column('weather_forecasts', 'is_daytime')
    op.drop_column('weather_forecasts', 'dew_point')
    op.drop_column('weather_forecasts', 'relative_humidity')
    # ### end Alembic commands ###
