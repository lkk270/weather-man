import requests
from core.settings import NWS_BASE_URL


class NWSApiClient:
    def __init__(self):
        self.base_url = NWS_BASE_URL
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "(weather-app, contact@example.com)"
        }

    def get_forecast_url(self, lat: float = 40.7816, lon: float = -73.9505) -> str:
        """Get the forecast URL for given coordinates"""
        points_url = f"{self.base_url}/points/{lat},{lon}"
        response = requests.get(points_url, headers=self.headers)
        response.raise_for_status()

        properties = response.json()['properties']
        return properties['forecastHourly'] if properties else None

    def fetch_weather_data(self, location: str, frequency: str = 'hourly') -> dict:
        forecast_url = self.get_forecast_url()

        response = requests.get(forecast_url, headers=self.headers)
        response.raise_for_status()
        return response.json()


def fetch_weather_data(location: str, frequency: str = 'hourly') -> dict:
    client = NWSApiClient()
    return client.fetch_weather_data(location, frequency)
