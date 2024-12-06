from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func
from database.models.base import Base


class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    my_temperature = Column(Float, nullable=True)
    relative_humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=True)
    dew_point = Column(Float, nullable=True)
    is_daytime = Column(Boolean, nullable=False)
    is_precipitating = Column(Boolean, nullable=False)
    # When the observation was made
    observed_for = Column(
        DateTime,
        nullable=False,
        server_default=func.now()

    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
