from sqlalchemy import Column, Integer, String, Float, DateTime, text
from database.models.base import Base


class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    my_temperature = Column(Float, nullable=True)
    relative_humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    dew_point = Column(Float, nullable=True)
    short_observation = Column(String, nullable=True)
    observed_time = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP AT TIME ZONE \'UTC\'')
    )
