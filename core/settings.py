import os
from dotenv import load_dotenv
from typing import Dict, NamedTuple

load_dotenv()


class LocationConfig(NamedTuple):
    name: str
    latitude: float
    longitude: float
    station_id: str  # STID for observations
    grid_id: str     # For NWS forecast API
    grid_x: int      # For NWS forecast API
    grid_y: int      # For NWS forecast API


LOCATIONS: Dict[str, LocationConfig] = {
    "NYC_CASTLE_1": LocationConfig(
        name="New York City",
        latitude=40.78333,
        longitude=-73.96667,
        station_id="KNYC",  # Central Park station
        grid_id="OKX",      # NWS grid ID for NYC
        grid_x=34,          # NWS grid coordinates
        grid_y=38
    ),
    "NYC_CASTLE_2": LocationConfig(
        name="New York City",
        latitude=40.7816,
        longitude=-73.9505,
        station_id="KNYC",  # Central Park station
        grid_id="OKX",      # NWS grid ID for NYC
        grid_x=35,          # NWS grid coordinates
        grid_y=38
    ),
    "MIA": LocationConfig(
        name="Miami, Miami International Airport",
        latitude=25.79056,
        longitude=-80.31639,
        station_id="KMIA",
        grid_id="MFL",
        grid_x=105,
        grid_y=51
    ),
}

NWS_FORECAST_BASE_URL = "https://api.weather.gov"
DATABASE_URL = os.getenv("DATABASE_URL")
NWS_OBSERVATION_BASE_URL = "https://api.mesowest.net/v2/stations/timeseries"
NWS_OBSERVATION_API_TOKEN = os.getenv('NWS_OBSERVATION_API_TOKEN')

if not NWS_OBSERVATION_API_TOKEN:
    raise ValueError(
        "NWS_OBSERVATION_API_TOKEN not found in environment variables")
