from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func, text
from database.models.base import Base
from datetime import datetime, timezone


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    relative_humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    dew_point = Column(Float, nullable=True)
    is_daytime = Column(Boolean, nullable=True)
    probability_of_precipitation = Column(Float, nullable=True)
    short_forecast = Column(String, nullable=True)
    forecast_time = Column(DateTime(timezone=True), nullable=False)
    is_correct = Column(Boolean, nullable=False, server_default=text('false'))
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP AT TIME ZONE \'UTC\'')
    )
