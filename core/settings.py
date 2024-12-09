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
    "DEN": LocationConfig(
        name="Denver, Denver International Airport",
        latitude=39.84658,
        longitude=-104.65622,
        station_id="KDEN",
        grid_id="BOU",
        grid_x=75,
        grid_y=66
    ),
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
        station_id="KNYC",
        grid_id="OKX",
        grid_x=35,
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
    "HOU": LocationConfig(
        name="Houston, Houston Hobby Airport",
        latitude=29.6375,
        longitude=-95.2825,
        station_id="KHOU",
        grid_id="HGX",
        grid_x=68,
        grid_y=91
    ),
    "PHL": LocationConfig(
        name="Philadelphia, Philadelphia International Airport",
        latitude=39.961978912353516,
        longitude=-75.14990234375,
        station_id="KPHL",
        grid_id="PHI",
        grid_x=50,
        grid_y=76
    ),
    "MDW": LocationConfig(
        name="Chicago, Chicago Midway Airport",
        latitude=41.78417,
        longitude=-87.75528,
        station_id="KMDW",
        grid_id="LOT",
        grid_x=72,
        grid_y=69
    ),
    "AUS": LocationConfig(
        name="Austin-Bergstrom International Airport",
        latitude=30.2,
        longitude=-97.68,
        station_id="KAUS",
        grid_id="EWX",
        grid_x=158,
        grid_y=88
    ),
}

NWS_FORECAST_BASE_URL = "https://api.weather.gov"
DATABASE_URL = os.getenv("DATABASE_URL")
NWS_OBSERVATION_BASE_URL = "https://api.mesowest.net/v2/stations/timeseries"
NWS_OBSERVATION_API_TOKEN = os.getenv('NWS_OBSERVATION_API_TOKEN')

if not NWS_OBSERVATION_API_TOKEN:
    raise ValueError(
        "NWS_OBSERVATION_API_TOKEN not found in environment variables")
