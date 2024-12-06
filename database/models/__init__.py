from database.models.base import Base
from database.models.forecast import WeatherForecast
from database.models.observation import WeatherObservation

__all__ = ['WeatherForecast', 'WeatherObservation', 'Base']
