import requests
from core.settings import NWS_OBSERVATION_BASE_URL, NWS_OBSERVATION_API_TOKEN, LOCATIONS


class ObservationAPIClient:
    def __init__(self):
        self.base_url = NWS_OBSERVATION_BASE_URL
        self.api_token = NWS_OBSERVATION_API_TOKEN

    def fetch_observations(self, location_id: str = "NYC") -> dict:
        """Fetch weather observations from the Mesowest API."""
        if location_id not in LOCATIONS:
            raise ValueError(f"Unknown location: {location_id}")

        location = LOCATIONS[location_id]

        params = {
            'STID': location.station_id,
            'showemptystations': '1',
            'units': 'temp|F,speed|mph,english',
            'recent': '4320',  # Last 3 days of observations
            'token': self.api_token,
            'complete': '1',
            'obtimezone': 'local'
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()

        data = response.json()

        if not data.get('STATION') or len(data['STATION']) == 0:
            raise Exception("No station data found in response")

        return data['STATION'][0]


def fetch_observation_data(location_id: str = "NYC") -> dict:
    """Convenience function to fetch observation data."""
    client = ObservationAPIClient()
    return client.fetch_observations(location_id)
