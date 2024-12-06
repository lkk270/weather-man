import requests
from core.settings import NWS_FORECAST_BASE_URL, LOCATIONS


class NWSApiClient:
    def __init__(self):
        self.base_url = NWS_FORECAST_BASE_URL
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "(weather-app, contact@example.com)"
        }

    def get_forecast_url(self, location_id: str = "NYC") -> str:
        """Get the forecast URL for given location"""
        if location_id not in LOCATIONS:
            raise ValueError(f"Unknown location: {location_id}")

        location = LOCATIONS[location_id]

        # Using grid endpoint directly instead of points endpoint for efficiency
        forecast_url = f"{self.base_url}/gridpoints/{location.grid_id}/{location.grid_x},{location.grid_y}/forecast/hourly"
        return forecast_url

    def fetch_forecast_data(self, location_id: str = "NYC") -> dict:
        forecast_url = self.get_forecast_url(location_id)

        response = requests.get(forecast_url, headers=self.headers)
        response.raise_for_status()
        return response.json()


def fetch_forecast_data(location_id: str = "NYC") -> dict:
    client = NWSApiClient()
    return client.fetch_forecast_data(location_id)
