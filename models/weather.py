from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
